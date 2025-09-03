from fastapi import FastAPI
from app.api.v1 import user_routers, auth_routers, minio_routers


app = FastAPI(title="CP")

app.include_router(user_routers.router, prefix="/api/v1")
app.include_router(auth_routers.router, prefix="/api/v1")
app.include_router(minio_routers.router, prefix="/api/v1")

