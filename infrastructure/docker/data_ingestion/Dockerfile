
FROM python:3.11-slim

# مسیر کاری
WORKDIR /app

# کپی فقط سورس این سرویس
COPY backend/services/data_ingestion /app/data_ingestion
COPY backend/shared /app/shared

# نصب وابستگی‌ها
RUN pip install --no-cache-dir fastapi uvicorn requests

# PYTHONPATH برای shared
ENV PYTHONPATH=/app

CMD ["uvicorn", "data_ingestion.main:app"]
