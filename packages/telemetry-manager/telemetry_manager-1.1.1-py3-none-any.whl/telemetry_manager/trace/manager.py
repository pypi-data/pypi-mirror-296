import typing as t

import opentelemetry
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SpanExporter,
)
from opentelemetry.trace import TracerProvider

from telemetry_manager.common import BaseManager, Resource, settings


class TraceManager(BaseManager):
    def __init__(
        self,
        otlp_endpoint: str,
        resource: Resource | opentelemetry.sdk.resources.Resource,
        provider: TracerProvider | None = None,
        exporter: t.Type[SpanExporter] | None = None,
        exporter_insecure: bool = True,
        exporter_settings: t.Mapping[str, t.Any] | None = None,
    ):
        super().__init__(otlp_endpoint, resource, exporter_settings)

        self.provider = provider or opentelemetry.sdk.trace.TracerProvider(
            resource=self.resource
        )

        if settings.TM_TRACE_IS_GRPC_EXPORTER_AVAILABLE:
            from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (  # pylint: disable=import-outside-toplevel # due to the nature of the import
                OTLPSpanExporter,
            )

            self.exporter = exporter or OTLPSpanExporter(
                self._otlp_endpoint,
                insecure=exporter_insecure,
                **self.exporter_settings,
            )
        elif settings.TM_TRACE_IS_HTTP_EXPORTER_AVAILABLE:
            from opentelemetry.exporter.otlp.proto.http.trace_exporter import (  # pylint: disable=import-outside-toplevel # due to the nature of the import
                OTLPSpanExporter,
            )

            self.exporter = exporter or OTLPSpanExporter(
                self._otlp_endpoint, **self.exporter_settings
            )
        else:
            self.exporter = exporter or ConsoleSpanExporter(
                self.resource.attributes.get("service.name", "n/a"),
                **self.exporter_settings,
            )

        self.provider.add_span_processor(BatchSpanProcessor(self.exporter))
