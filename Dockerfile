FROM python:3.11-slim

WORKDIR /app

# Создаем папку для логов
RUN mkdir -p /app/logs

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY tg_bot.py .

# Создаем пользователя для безопасности
RUN useradd -m -u 1000 botuser && chown -R botuser:botuser /app
USER botuser

CMD ["python", "tg_bot.py"]