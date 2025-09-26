# Базовый образ
FROM python:3.11-slim

# Установка системных пакетов для компиляции зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копируем только requirements.txt для кэширования зависимостей
COPY requirements.txt .

# Установка зависимостей с приоритетом бинарных колес
RUN pip install --upgrade pip \
    && pip install --prefer-binary -r requirements.txt

# Копируем исходный код
COPY . /app/app

# Экспонируем порт FastAPI
EXPOSE 8000

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
