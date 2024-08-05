FROM python:3.12

LABEL authors="OstWinD"

# Установка Poetry
RUN pip install poetry

# Установка рабочей директории
WORKDIR /app

# Копирование файлов зависимостей
COPY pyproject.toml poetry.lock /app/

# Настройка Poetry
RUN poetry config virtualenvs.path --unset
RUN poetry config virtualenvs.in-project true

# Установка зависимостей
RUN poetry install --no-root --no-dev

# Копирование всего проекта в рабочую директорию
COPY . /app

# Установка переменной окружения PATH
ENV PATH="/app/.venv/bin:$PATH"

RUN chmod a+x /app/docker/*.sh
