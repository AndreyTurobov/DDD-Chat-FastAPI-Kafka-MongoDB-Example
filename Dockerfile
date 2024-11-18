# Этап сборки зависимостей
FROM python:3.12.2-slim-bullseye AS builder

# Копирование файлов poetry
COPY poetry.lock pyproject.toml ./

# Установка poetry и формирование файла с зависимостями
RUN python -m pip install poetry==1.8.2 &&\
    poetry export --without-hashes -o requirements.prod.txt && \
    poetry export --with=dev -o requirements.dev.txt --without-hashes

# Этап сборки приложения
FROM python:3.12.2-slim-bullseye AS dev

# Создание рабочей директории
WORKDIR /app

# Установка переменных окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Копирование установленных зависимостей из builder
COPY --from=builder requirements.dev.txt /app

# Установка системных зависимостей
RUN apt update -y && \
    apt install -y --no-install-recommends python3-dev gcc musl-dev && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.dev.txt && \
    apt autoremove -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# Копирование кода приложения
COPY /app/ /app/**

EXPOSE 8000