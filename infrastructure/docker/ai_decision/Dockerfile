
FROM python:3.11-slim

# مسیر کاری
WORKDIR /app

# کپی فقط سورس این سرویس
COPY backend/services/ai_decision /app/ai_decision
COPY backend/shared /app/shared

# نصب وابستگی‌ها
RUN pip install --no-cache-dir fastapi uvicorn requests

# PYTHONPATH برای shared
ENV PYTHONPATH=/app

CMD ["uvicorn", "ai_decision.main:app"]
