FROM sfs_base:latest

WORKDIR /app

COPY backend/services/data_ingestion /app/backend/services/data_ingestion

RUN pip install --no-cache-dir fastapi uvicorn requests

CMD ["uvicorn","backend.services.data_ingestion.main:app","--host", "0.0.0.0","--port", "8001"]
