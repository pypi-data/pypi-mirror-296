"""Telemetry manager is a wrapper on top of an opentelemetry library
that removes part of the boilerplate from projects"""

import logging
import sys

from telemetry_manager.common import Resource, settings
from telemetry_manager.trace import TraceManager
from telemetry_manager.log import LogManager
from telemetry_manager.metric import MetricManager
from telemetry_manager.manager import TelemetryManager
import importlib.util as importlib_util

logger = logging.getLogger(__name__)

__all__ = [
    "LogManager",
    "MetricManager",
    "Resource",
    "TelemetryManager",
    "TraceManager",
]

_OPTIONAL_DEPS = [
    {
        "beautiful_name": "gRPC traces exporter",
        "module_name": "opentelemetry.exporter.otlp.proto.grpc.trace_exporter",
        "settings_var": "TM_TRACE_IS_GRPC_EXPORTER_AVAILABLE",
    },
    {
        "beautiful_name": "HTTP traces exporter",
        "module_name": "opentelemetry.exporter.otlp.proto.http.trace_exporter",
        "settings_var": "TM_TRACE_IS_HTTP_EXPORTER_AVAILABLE",
    },
    {
        "beautiful_name": "gRPC logs exporter",
        "module_name": "opentelemetry.exporter.otlp.proto.grpc._log_exporter",
        "settings_var": "TM_LOG_IS_GRPC_EXPORTER_AVAILABLE",
    },
    {
        "beautiful_name": "HTTP logs exporter",
        "module_name": "opentelemetry.exporter.otlp.proto.http._log_exporter",
        "settings_var": "TM_LOG_IS_HTTP_EXPORTER_AVAILABLE",
    },
    {
        "beautiful_name": "gRPC metrics exporter",
        "module_name": "opentelemetry.exporter.otlp.proto.grpc.metric_exporter",
        "settings_var": "TM_METRIC_IS_GRPC_EXPORTER_AVAILABLE",
    },
    {
        "beautiful_name": "HTTP metrics exporter",
        "module_name": "opentelemetry.exporter.otlp.proto.http.metric_exporter",
        "settings_var": "TM_METRIC_IS_HTTP_EXPORTER_AVAILABLE",
    },
]
if not settings.TM_CHECKED_IMPORTS:
    for dep in _OPTIONAL_DEPS:
        logger.debug(
            "Checking dependencies: %s", dep.get("beautiful_name")
        )
        module_name = dep["module_name"]
        settings_var: str = dep["settings_var"]

        if module_name in sys.modules:
            logger.info(
                "%s is already in sys.modules", dep.get("beautiful_name")
            )
            setattr(settings, settings_var, True)
        elif (spec := importlib_util.find_spec(module_name)) is not None:
            logger.info(
                "%s is installed, but not in sys.modules",
                dep.get("beautiful_name"),
            )
            setattr(settings, settings_var, True)
        else:
            logger.warning("%s not found", dep.get("beautiful_name"))

settings.TM_CHECKED_IMPORTS = True
