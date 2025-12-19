FROM python:3.11-slim

WORKDIR /app

COPY backend/services/ai_decision /app
COPY backend/shared /app/shared

RUN pip install --no-cache-dir fastapi uvicorn requests

ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8004"]
