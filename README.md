Создать миграцию:

docker compose run --rm fastapi alembic revision --autogenerate -m "новая миграция"


Применить ее к базе:

docker compose run --rm fastapi alembic upgrade head


запуск прометеуса для сбора метрик

prometheus --config.file=prometheus.yml

