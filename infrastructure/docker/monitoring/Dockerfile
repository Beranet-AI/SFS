
#FROM python:3.11-slim

#WORKDIR /app

#COPY backend/services/monitoring /app/monitoring
#COPY backend/shared /app/shared

#ENV PYTHONPATH=/app

#WORKDIR /app/monitoring

#RUN pip install --no-cache-dir fastapi uvicorn requests

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]




FROM python:3.11-slim

# مسیر کاری
WORKDIR /app

# کپی فقط سورس این سرویس
COPY backend/services/monitoring /app/monitoring
COPY backend/shared /app/shared

# نصب وابستگی‌ها
RUN pip install --no-cache-dir fastapi uvicorn requests

# PYTHONPATH برای shared
ENV PYTHONPATH=/app

CMD ["uvicorn", "monitoring.main:app"]
