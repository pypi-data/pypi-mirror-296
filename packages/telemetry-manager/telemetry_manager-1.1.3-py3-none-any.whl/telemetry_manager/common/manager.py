import abc

import opentelemetry
import typing as t
from telemetry_manager.common import Resource


class BaseManager(abc.ABC):
    def __init__(
        self,
        otlp_endpoint: str,
        resource: Resource | opentelemetry.sdk.resources.Resource,
        exporter_settings: t.Mapping[str, t.Any] | None = None,
    ):
        self._otlp_endpoint: str = otlp_endpoint
        self.resource = resource or Resource().get()
        self.exporter_settings = exporter_settings or {}
