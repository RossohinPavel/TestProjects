from os import getenv


class PostgresConfig:
    HOST: str = str(getenv("POSTGRES_HOST", ""))
    PORT: str = str(getenv("POSTGRES_PORT", ""))
    USER: str = str(getenv("POSTGRES_USER", ""))
    PASS: str = str(getenv("POSTGRES_PASSWORD", ""))
    NAME: str = str(getenv("POSTGRES_NAME", ""))

    @property
    def DATABASE_ASYNC_URL(self) -> str:
        return f'asyncpg://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}'


sqlite = 'sqlite://db.sqlite3'


TORTOISE_CONFIG = {
    "connections": {"default": PostgresConfig().DATABASE_ASYNC_URL},
    "apps": {
        "models": {
            "models": ["orm.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
