# Базовий образ Python
FROM python:3.14

# Робоча директорія
ENV APP_HOME=/app
WORKDIR $APP_HOME

# Встановлюємо uv
RUN pip install --no-cache-dir uv --root-user-action=ignore

# Копіюємо проєкт
COPY . .

# ставимо залежності через pyproject.toml
RUN uv sync

# порт сервера
EXPOSE 3000

# запуск
CMD ["uv", "run", "main.py"]