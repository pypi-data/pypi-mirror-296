from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
        BatchSpanProcessor,
        ConsoleSpanExporter,
    )

from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.trace import Status, StatusCode
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
import logging

from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter,
)

def hello():
    print("Hello, World from otel-sdk-kfc!")

def CreateTracer(service_name, trace_name, collector_endpoint):
    resource = Resource.create({"service.name": service_name})
    trace.set_tracer_provider(TracerProvider(resource=resource))
    tracer = trace.get_tracer(trace_name)

    otlp_span_exporter = OTLPSpanExporter(endpoint=collector_endpoint+"/v1/traces")
    span_processor = BatchSpanProcessor(otlp_span_exporter)

    trace.get_tracer_provider().add_span_processor(span_processor)

    return tracer

def CreateMeter(service_name, meter_name, collector_endpoint):
    resource = Resource.create({"service.name": service_name})
    otlp_metric_exporter = OTLPMetricExporter(endpoint=collector_endpoint+"/v1/metrics", insecure=True)
    reader = PeriodicExportingMetricReader(otlp_metric_exporter)
    metrics.set_meter_provider(MeterProvider(resource=resource, metric_readers=[reader]))
    meter = metrics.get_meter(meter_name)

    return meter

def LogHandler(service_name, collector_endpoint):
    # Create and set the logger provider
    logger_provider = LoggerProvider(
        resource=Resource.create(
            {
                "service.name": service_name,
            }
        ),
    )

    set_logger_provider(logger_provider)

    exporter = OTLPLogExporter(endpoint=collector_endpoint+"/v1/logs", insecure=True) # endpoint=collector_endpoint+"/v1/logs"
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
    handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)

    logging.getLogger().addHandler(handler)