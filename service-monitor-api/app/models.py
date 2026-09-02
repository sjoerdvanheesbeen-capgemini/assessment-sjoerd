from dataclasses import dataclass


@dataclass
class ServiceConfig:
    name: str
    type: str
    namespace: str
    port: int

    path: str | None = None
    database: str | None = None