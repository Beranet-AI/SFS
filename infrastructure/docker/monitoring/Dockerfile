#FROM python:3.11-slim

#WORKDIR /app

# کپی کل سرویس
#COPY backend/services/monitoring /app

# مهم: پایتون باید /app را بشناسد
#ENV PYTHONPATH=/app

#RUN pip install --no-cache-dir fastapi uvicorn

#CMD ["uvicorn", "monitoring.main:app", "--host", "0.0.0.0", "--port", "8002"]



FROM python:3.11-slim

WORKDIR /app

COPY backend/services/monitoring /app/monitoring
COPY backend/shared /app/shared

ENV PYTHONPATH=/app

WORKDIR /app/monitoring

RUN pip install --no-cache-dir fastapi uvicorn

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
