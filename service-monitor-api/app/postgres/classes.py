import os

from attr import dataclass

from models import ServiceConfig

@dataclass
class PostgresqlSettings:
    postgresql_host: str
    postgresql_port: int
    postgresql_db: str
    postgresql_user: str
    postgresql_password: str

    @classmethod
    def load(cls, service_config: ServiceConfig | None):
        if service_config:
            return cls(
                postgresql_host=f"{service_config.name}.{service_config.namespace}.svc.cluster.local",
                postgresql_port=service_config.port,
                postgresql_db=service_config.database or "",
                postgresql_user=os.getenv("POSTGRES_USER", ""),
                postgresql_password=os.getenv("POSTGRES_PASSWORD", ""),
            )
        raise ValueError("A PostgreSQL service configuration is required")