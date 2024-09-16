import asyncio
from contextlib import asynccontextmanager, contextmanager
from functools import wraps

import httpx
import requests
from django.core.handlers.wsgi import WSGIRequest
from django.core.signals import request_started
from fastapi import FastAPI, Request
from flask import Flask
from flask import request as flask_request
from loguru import logger
from openinference.semconv.resource import ResourceAttributes
from opentelemetry import context as context_api
from opentelemetry import trace
from opentelemetry.context import Context, get_current, get_value, set_value
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.threading import ThreadingInstrumentor
from opentelemetry.propagate import extract
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.resources import Resource
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

from acutracer.exporters.jaeger_exporter import CustomJaegerExporter

GLOBAL_SPAN = trace.Span

class WebAPIInstrumentor:
    def __init__(self, name="acutracer", tracer=None):
        self.tracer_provider = trace_sdk.TracerProvider(
            resource=Resource.create({"service.name": name}),
            span_limits=trace_sdk.SpanLimits(max_attributes=10_000),
        )
        jeager_exporter = CustomJaegerExporter()
        self.tracer_provider.add_span_processor(jeager_exporter.get_processor())

        trace.set_tracer_provider(self.tracer_provider)
        self.tracer = tracer or trace.get_tracer(__name__)

    def instrument_requests(self):
        original_send = requests.Session.send

        @wraps(original_send)
        def instrumented_send(session, request, **kwargs):
            # get the current/parent span
            current_span = trace.get_current_span()
            parent_context = current_span.get_span_context() if current_span else None

            with self.tracer.start_as_current_span(f"Requests {request.method} {request.url}") as span:
                headers = request.headers
                headers.update({
                    "X-acuvity-trace-id": f"{span.get_span_context().trace_id:032x}",
                    "X-acuvity-span-id": f"{span.get_span_context().span_id:016x}"
                })
                # Add parent span ID if it exists
                parent_id = get_value('acutracer-root-span-id')
                if parent_id and parent_id != trace.INVALID_SPAN_ID:
                    headers["X-acuvity-parent-id"] = parent_id
                # if parent_context and parent_context.span_id != trace.INVALID_SPAN_ID:
                #     headers["X-acuvity-parent-id"] = f"{parent_context.span_id:016x}"

                response = original_send(session, request, **kwargs)
                span.set_attribute("http.status_code", response.status_code)
                span.set_attribute("http.response_content_length", len(response.content))
                return response

        requests.Session.send = instrumented_send

    def instrument_httpx(self):
        original_send = httpx.Client.send
        original_async_send = httpx.AsyncClient.send

        @wraps(original_send)
        def instrumented_send(client, request, **kwargs):
            # We don't trace the testclients
            if request.headers.get('user-agent') == 'testclient':
                return original_send(client, request, **kwargs)

            # get the current/parent span
            current_span = trace.get_current_span()
            parent_context = current_span.get_span_context() if current_span else None

            parent_id = get_value('acutracer-root-span-id')
            logger.info(f"\n val for key:acutracer-root-span-id from context: {parent_id} for request: {request.headers}\n")

            with self.tracer.start_as_current_span(f"HTTP-SYNC {request.method} {request.url}") as span:
                headers = request.headers
                headers.update({
                    "X-acuvity-trace-id": f"{span.get_span_context().trace_id:032x}",
                    "X-acuvity-span-id": f"{span.get_span_context().span_id:016x}"
                })
                # Add parent span ID if it exists
                parent_id = get_value('acutracer-root-span-id')
                if parent_id and parent_id != trace.INVALID_SPAN_ID:
                    headers["X-acuvity-parent-id"] = parent_id

                logger.info(f"httpx send {request.method} {request.url} {request.headers} {request.content}\n")
                response = original_send(client, request, **kwargs)
                span.set_attribute("http.status_code", response.status_code)

                return response

        @wraps(original_async_send)
        async def instrumented_async_send(client, request, **kwargs):
            # We don't trace the testclients
            if request.headers.get('user-agent') == 'testclient':
                return original_send(client, request, **kwargs)

            # get the current/parent span
            current_span = trace.get_current_span()
            parent_context = current_span.get_span_context() if current_span else None

            with self.tracer.start_as_current_span(f"HTTP-ASYNC {request.method} {request.url}") as span:
                headers = request.headers
                headers.update({
                    "X-acuvity-trace-id": f"{span.get_span_context().trace_id:032x}",
                    "X-acuvity-span-id": f"{span.get_span_context().span_id:016x}"
                })
                # Add parent span ID if it exists
                parent_id = get_value('acutracer-root-span-id')
                if parent_id and parent_id != trace.INVALID_SPAN_ID:
                    headers["X-acuvity-parent-id"] = parent_id
                # if parent_context and parent_context.span_id != trace.INVALID_SPAN_ID:
                #     headers["X-acuvity-parent-id"] = f"{parent_context.span_id:016x}"

                response = await original_async_send(client, request, **kwargs)
                span.set_attribute("http.status_code", response.status_code)
                #span.set_attribute("http.response_content_length", len(response.content))
                return response

        httpx.Client.send = instrumented_send
        httpx.AsyncClient.send = instrumented_async_send

    def instrument(self, app: FastAPI):
        FastAPIInstrumentor.instrument_app(app)
        ThreadingInstrumentor().instrument()

        @app.middleware("http")
        async def add_parent_trace(request: Request, call_next):
            logger.info(f"\n add_parent_trace for request {request.url} {request.headers}, tracer: {self.tracer}")

            current_span = trace.get_current_span()
            parent_context = current_span.get_span_context() if current_span else None
            if parent_context is None:
                logger.info("\n Parent context missing")
            else:
                logger.info(f"\n parent context: {parent_context}")

            # Extract the existing context from headers
            # Check if X-acuvity-trace-id exists in headers
            existing_trace_id = request.headers.get("X-acuvity-trace-id")
            existing_span_id = request.headers.get("X-acuvity-span-id")
            token = object()
            if existing_trace_id and existing_span_id:
                # If X-acuvity-trace-id exists, use it to create a new context and attach it
                try:
                    trace_id = int(existing_trace_id, 16)
                    span_id = int(existing_span_id, 16)
                    new_context = trace.set_span_in_context(
                        trace.NonRecordingSpan(trace.SpanContext(
                            trace_id=trace_id,
                            span_id=span_id,
                            is_remote=True,
                            trace_flags=trace.TraceFlags(0x1)
                        )), get_current()
                    )
                    # Only update the context if we successfully created a new one
                    ctx_with_acu_root_span = set_value("acutracer-root-span-id", existing_span_id, new_context)
                    token = context_api.attach(ctx_with_acu_root_span)
                except ValueError:
                    logger.warning(f"Invalid X-acuvity-trace-id: {existing_trace_id}")
            else:
                logger.warning("\nAcuvity headers are not present")

            # span_context = trace.get_current_span().get_span_context()
            # ctx = set_value("acutracer-root-span-id", f"{span_context.span_id:016x}")
            # tok = context_api.attach(ctx)

            with self.tracer.start_as_current_span(
                f"APP http_request {request.method} {request.url}"
            ) as span:
                logger.info(f"starting span {span.get_span_context()}")

                # Add custom headers to the request state
                request.state.custom_headers = {
                    "X-acuvity-trace-id": f"{span.get_span_context().trace_id:032x}",
                    "X-acuvity-span-id": f"{span.get_span_context().span_id:016x}"
                }

                response = await call_next(request)

                # Always dettach.
                context_api.detach(token)
                return response

        self.instrument_httpx()
        self.instrument_requests()
        return self.tracer

    def instrument_gradio(self, blocks):
        logger.info("Instrumenting Gradio app")
        original_process_api = blocks.process_api
        ThreadingInstrumentor().instrument()

        @wraps(original_process_api)
        async def instrumented_process_api(*args, **kwargs):
            logger.debug("instrumented process_api")
            with self.tracer.start_as_current_span("gradio_event") as span:
                logger.debug(f" instrumented_process_api args {kwargs}")
                request = kwargs.get('request')
                headers = dict(request.headers)
                headers.update({
                    "X-acuvity-trace-id": f"{span.get_span_context().trace_id:032x}",
                    "X-acuvity-span-id": f"{span.get_span_context().span_id:016x}"
                })
                fn_index = kwargs.get('fn_index', 'unknown')
                span.set_attribute("event_name", f"event_{fn_index}")
                try:
                    result = await original_process_api(*args, **kwargs)
                    logger.debug("DONE processing the instrumented_process_api \n")
                    return result
                except Exception as e:
                    logger.error(f"Error in process_api: {str(e)}")
                    span.record_exception(e)
                    raise

        blocks.process_api = instrumented_process_api
        self.instrument_httpx()
        self.instrument_requests()
        logger.info("Gradio app instrumentation complete")

    def instrument_flask(self, app: Flask):
        FlaskInstrumentor().instrument_app(app)
        ThreadingInstrumentor().instrument()

        @app.before_request
        def before_request():
            logger.trace(f"\n In before_request for Flask, tracer: {self.tracer}")
            with self.tracer.start_as_current_span(f"Flask http_request {flask_request.method} {flask_request.url}") as span:
                context = TraceContextTextMapPropagator().extract(flask_request.headers)
                trace.set_span_in_context(span, context)

                flask_request.custom_headers = {
                    "X-acuvity-trace-id": f"{span.get_span_context().trace_id:032x}",
                    "X-acuvity-span-id": f"{span.get_span_context().span_id:016x}"
                }
        self.instrument_httpx()
        self.instrument_requests()
        return self.tracer

    def instrument_django(self):
        DjangoInstrumentor().instrument()
        ThreadingInstrumentor().instrument()

        def start_span(sender, **kwargs):
            request = kwargs.get('request', None)
            if not isinstance(request, WSGIRequest):
                return

            with self.tracer.start_as_current_span(f"Django http_request {request.method} {request.path}") as span:
                context = TraceContextTextMapPropagator().extract(request.META)
                trace.set_span_in_context(span, context)

                request.custom_headers = {
                    "X-acuvity-trace-id": f"{span.get_span_context().trace_id:032x}",
                    "X-acuvity-span-id": f"{span.get_span_context().span_id:016x}"
                }

        request_started.connect(start_span)

        self.instrument_httpx()
        self.instrument_requests()

        return self.tracer
