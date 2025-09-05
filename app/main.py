from fastapi import FastAPI, Request, HTTPException
from starlette.responses import PlainTextResponse
from prometheus_fastapi_instrumentator import Instrumentator
from app.core.config import settings
from app.api.v1 import user_routers, auth_routers, minio_routers

app = FastAPI(title="CP")

# Настраиваем инструментатор сразу после создания app
instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True
)
instrumentator.instrument(app)  # добавляем middleware
# не вызываем expose(app) — используем свой endpoint

# Сохраняем в state для доступа из /metrics
app.state.instrumentator = instrumentator

@app.get("/metrics")
async def metrics(request: Request):
    auth = request.headers.get("Authorization")
    if auth != f"Bearer {settings.METRICS_TOKEN}":
        raise HTTPException(status_code=403, detail="Forbidden")

    instrumentator: Instrumentator = request.app.state.instrumentator
    registry = instrumentator.registry

    from prometheus_client import generate_latest
    return PlainTextResponse(generate_latest(registry), media_type="text/plain")


# Роутеры
app.include_router(user_routers.router, prefix="/api/v1")
app.include_router(auth_routers.router, prefix="/api/v1")
app.include_router(minio_routers.router, prefix="/api/v1")
