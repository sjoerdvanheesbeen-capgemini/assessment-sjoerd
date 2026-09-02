import os
from dataclasses import dataclass
from pathlib import Path

import yaml

from models import ServiceConfig


def load_services(file_path: str | Path) -> list[ServiceConfig]:
    with Path(file_path).open(encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    return [
        ServiceConfig(
            name=service["name"],
            type=service["type"],
            namespace=service["namespace"],
            port=service["port"],
            path=service.get("health_path"),
            database=service.get("db_name"),
        )
        for service in data["services"]
    ]


def get_service(
    service_name: str,
    services: list[ServiceConfig],
) -> ServiceConfig | None:
    return next(
        (service for service in services if service.name == service_name),
        None,
    )

services = load_services("config/services.yaml")