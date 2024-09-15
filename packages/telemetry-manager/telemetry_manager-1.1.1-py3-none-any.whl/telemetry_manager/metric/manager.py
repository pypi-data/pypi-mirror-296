import typing as t
import time

import opentelemetry
from opentelemetry import metrics
from opentelemetry.metrics import Meter, Observation, CallbackOptions
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics._internal.export import (
    MetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.resources import Resource


import psutil

from telemetry_manager.common import BaseManager, settings


class MetricManager(BaseManager):
    def __init__(
        self,
        otlp_endpoint: str,
        resource: Resource | opentelemetry.sdk.resources.Resource,
        provider: MeterProvider | None = None,
        exporter: t.Type[MetricExporter] | None = None,
        exporter_insecure: bool = True,
        exporter_settings: t.Mapping[str, t.Any] | None = None,
    ):
        super().__init__(otlp_endpoint, resource, exporter_settings)

        exporter_settings = exporter_settings or {}

        # Initialize the exporter
        if settings.TM_METRIC_IS_GRPC_EXPORTER_AVAILABLE:
            from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
                OTLPMetricExporter,
            )

            self.exporter = exporter or OTLPMetricExporter(
                endpoint=self._otlp_endpoint,
                insecure=exporter_insecure,
                **self.exporter_settings,
            )
        elif settings.TM_METRIC_IS_HTTP_EXPORTER_AVAILABLE:
            from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
                OTLPMetricExporter as OTLPHTTPMetricExporter,
            )

            self.exporter = exporter or OTLPHTTPMetricExporter(
                endpoint=self._otlp_endpoint,
                **self.exporter_settings,
            )
        else:
            raise Exception("No suitable metric exporter available")

        metric_reader = PeriodicExportingMetricReader(
            self.exporter, export_interval_millis=1000
        )

        self.provider = provider or MeterProvider(
            resource=self.resource, metric_readers=[metric_reader]
        )

        metrics.set_meter_provider(self.provider)

    def _cpu_usage_callback(self, options: CallbackOptions):
        usage = psutil.cpu_percent(interval=None)
        return [Observation(value=usage)]

    def _memory_usage_callback(self, options: CallbackOptions):
        usage = psutil.virtual_memory().percent
        return [Observation(value=usage)]

    def _disk_usage_callback(self, options: CallbackOptions):
        usage = psutil.disk_usage("/").percent
        return [Observation(value=usage)]

    def _network_bytes_sent_callback(self, options: CallbackOptions):
        bytes_sent = psutil.net_io_counters().bytes_sent
        return [Observation(value=bytes_sent)]

    def _network_bytes_recv_callback(self, options: CallbackOptions):
        bytes_recv = psutil.net_io_counters().bytes_recv
        return [Observation(value=bytes_recv)]

    def _register_gauges(self, meter: Meter):
        self.cpu_usage_gauge = meter.create_observable_gauge(
            name="system_cpu_usage_percent",
            callbacks=[self._cpu_usage_callback],
            description="System CPU usage in percent",
            unit="%",
        )

        self.memory_usage_gauge = meter.create_observable_gauge(
            name="system_memory_usage_percent",
            callbacks=[self._memory_usage_callback],
            description="System memory usage in percent",
            unit="%",
        )

        self.disk_usage_gauge = meter.create_observable_gauge(
            name="system_disk_usage_percent",
            callbacks=[self._disk_usage_callback],
            description="System disk usage in percent",
            unit="%",
        )

        self.network_bytes_sent_counter = meter.create_observable_counter(
            name="system_network_bytes_sent_total",
            callbacks=[self._network_bytes_sent_callback],
            description="Total bytes sent over the network",
            unit="bytes",
        )

        self.network_bytes_recv_counter = meter.create_observable_counter(
            name="system_network_bytes_received_total",
            callbacks=[self._network_bytes_recv_callback],
            description="Total bytes received over the network",
            unit="bytes",
        )
