"""Settings module."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings class. Stores variables for manager"""

    TM_CHECKED_IMPORTS: bool = False

    TM_TRACE_IS_GRPC_EXPORTER_AVAILABLE: bool = False
    TM_TRACE_IS_HTTP_EXPORTER_AVAILABLE: bool = False

    TM_LOG_IS_GRPC_EXPORTER_AVAILABLE: bool = False
    TM_LOG_IS_HTTP_EXPORTER_AVAILABLE: bool = False

    TM_METRIC_IS_GRPC_EXPORTER_AVAILABLE: bool = False
    TM_METRIC_IS_HTTP_EXPORTER_AVAILABLE: bool = False


settings = Settings()
