
FROM python:3.11-slim

# مسیر کاری
WORKDIR /app

# کپی فقط سورس این سرویس
COPY backend/services/edge_controller /app/edge_controller
COPY backend/shared /app/shared

# نصب وابستگی‌ها
RUN pip install --no-cache-dir fastapi uvicorn requests

# PYTHONPATH برای shared
ENV PYTHONPATH=/app

CMD ["uvicorn", "edge_controller.main:app"]
