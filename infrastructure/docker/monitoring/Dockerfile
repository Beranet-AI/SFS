FROM sfs_base:latest

WORKDIR /app

COPY backend/services/monitoring /app/backend/services/monitoring

RUN pip install --no-cache-dir fastapi uvicorn requests pydantic-settings httpx

CMD ["uvicorn","backend.services.monitoring.main:app","--host", "0.0.0.0","--port", "8002"]
