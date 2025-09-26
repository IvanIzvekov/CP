from contextlib import asynccontextmanager
from typing import AsyncGenerator

import aioboto3

from app.core.config import settings

session = aioboto3.Session()


@asynccontextmanager
async def get_s3_client() -> AsyncGenerator:
    async with session.client(
        "s3",
        endpoint_url=settings.MINIO_ENDPOINT,
        aws_access_key_id=settings.MINIO_ROOT_USER,
        aws_secret_access_key=settings.MINIO_ROOT_PASSWORD,
    ) as client:
        yield client
