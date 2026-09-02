from attr import dataclass

from models import ServiceConfig

def get_bearer_token() -> str:
    return "token"

@dataclass
class RESTAPISettings:
    url: str
    bearer_token: str

    @classmethod
    def load(cls, service_config: ServiceConfig | None):
        if service_config:
            return cls(
                url=f"{service_config.name}.{service_config.namespace}.svc.cluster.local:{service_config.port}",
                bearer_token=get_bearer_token()
            )
        raise ValueError("A service configuration is required")