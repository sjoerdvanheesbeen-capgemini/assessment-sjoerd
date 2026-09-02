import httpx

from config import services, get_service
from restapi.classes import RESTAPISettings


class RestChecker():

    def __init__(self, name: str):
        self.name = name
        service_config = get_service(name, services)
        if service_config is None:
            raise ValueError(f"Unknown RESTAPI service: {name}")

        self.config = RESTAPISettings.load(service_config)

    async def check(self) -> dict:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.config.url,
                    headers={
                        "Authorization": f"Bearer {self.config.bearer_token}",
                    },
                    timeout=5,
                )

            return {
                "name": self.name,
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "status_code": response.status_code
            }

        except Exception as ex:
            return {
                "name": self.name,
                "status": "unhealthy",
                "error": str(ex)
            }