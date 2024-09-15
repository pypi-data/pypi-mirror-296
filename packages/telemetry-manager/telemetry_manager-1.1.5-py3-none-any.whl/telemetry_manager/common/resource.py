import pathlib
from datetime import datetime
import logging

from opentelemetry.sdk.resources import Resource as OpenTelemetryResource

import httpx

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(
    level=logging.DEBUG,
)


class Resource:
    def __init__(
        self,
        service: str = pathlib.Path(__file__).parent.name,
        version: str = "v1.1.1",
        image: str = "n/a",
        host: str | None = None,
        start_time: datetime | None = None,
        request_host_ip: bool = False,
        image_version: str | None = None,
    ) -> None:
        """
        :param service: Software name
        :param version: Software version
        :param image: Container image name
        :param host: Machine ip address
        :param start_time: Initialization timestamp
        :param request_host_ip: Whether to request host ip
        """
        self.service = service
        self.version = version
        self.image = image
        self.host = (
            host or httpx.get("https://ifconfig.me").text
            if request_host_ip
            else "localhost"
        )
        self.start_time = start_time or datetime.now()
        self.image_version = image_version or version

    def get(self) -> OpenTelemetryResource:
        return OpenTelemetryResource(
            attributes={
                "service.name": self.service,
                "service.version": self.service,
                "image.name": self.service,
                "image.version": self.image_version,
                "host.address": self.host,
                "host.start_time": str(self.start_time),
            }
        )


def main() -> int:
    return 0


if __name__ == "__main__":
    main()
