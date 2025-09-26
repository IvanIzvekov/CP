from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    JWT_SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    # для Redis
    REDIS_HOST: str
    REDIS_PASSWORD: str
    REDIS_PORT: int

    # для Minio
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_ENDPOINT: str

    # prometheus
    METRICS_TOKEN: str

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


settings = Settings()
