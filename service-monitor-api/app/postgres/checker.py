import psycopg2

from postgres.classes import PostgresqlSettings
from config import services, get_service


class PostgresqlChecker():

    def __init__(self, db_name: str):
        self.name = db_name
        service_config = get_service(db_name, services)
        if service_config is None:
            raise ValueError(f"Unknown PostgreSQL service: {db_name}")

        self.config = PostgresqlSettings.load(service_config)

    async def check(self) -> dict:
        try:
            with psycopg2.connect(
                database=self.config.postgresql_db,
                user=self.config.postgresql_user,
                password=self.config.postgresql_password,
                host=self.config.postgresql_host,
                port=self.config.postgresql_port
            ) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1") 

            return {
                "name": self.name,
                "status": "healthy"
            }

        except Exception as ex:
            return {
                "name": self.name,
                "status": "unhealthy",
                "error": str(ex)
            }