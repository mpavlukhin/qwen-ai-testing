FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование приложения
COPY run.py .
COPY templates/ ./templates/

# Открываем порт
EXPOSE 8000

# Запуск приложения
CMD ["python", "run.py", "--host", "0.0.0.0", "--port", "8000"]
