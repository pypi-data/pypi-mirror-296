import typing as t

import opentelemetry
from opentelemetry._logs import LoggerProvider
from opentelemetry.sdk._logs.export import (
    BatchLogRecordProcessor,
    ConsoleLogExporter,
    LogExporter,
)

from telemetry_manager.common import BaseManager, Resource, settings


class LogManager(BaseManager):
    """LogManager is a manager for logging part of the telemetry service."""

    def __init__(
        self,
        otlp_endpoint: str,
        resource: Resource | opentelemetry.sdk.resources.Resource,
        provider: LoggerProvider | None = None,
        exporter: t.Type[LogExporter] | None = None,
        exporter_insecure: bool = True,
        exporter_settings: t.Mapping[str, t.Any] | None = None,
    ):
        """
        :param otlp_endpoint: Opentelemetry collector endpoint
        :param resource: Current resource's definition
        :param provider: Opentelemetry LoggerProvider
        :param exporter: Opentelemetry LoggerExpornet
        :param exporter_insecure: Allow insecure exporter connection
        :param exporter_settings: Custom settings for exporter
        """
        super().__init__(otlp_endpoint, resource, exporter_settings)

        self.provider = provider or opentelemetry.sdk._logs.LoggerProvider(
            resource=self.resource
        )

        if settings.TM_LOG_IS_GRPC_EXPORTER_AVAILABLE:
            from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (  # pylint: disable=import-outside-toplevel # due to the nature of the import
                OTLPLogExporter,
            )

            self.exporter = exporter or OTLPLogExporter(
                self._otlp_endpoint,
                insecure=exporter_insecure,
                **self.exporter_settings,
            )
        elif settings.TM_LOG_IS_HTTP_EXPORTER_AVAILABLE:
            from opentelemetry.exporter.otlp.proto.http._log_exporter import (  # pylint: disable=import-outside-toplevel # due to the nature of the import
                OTLPLogExporter,
            )

            self.exporter = exporter or OTLPLogExporter(
                self._otlp_endpoint, **self.exporter_settings
            )
        else:
            self.exporter = exporter or ConsoleLogExporter(
                **self.exporter_settings
            )

        self.provider.add_log_record_processor(
            BatchLogRecordProcessor(self.exporter)
        )
