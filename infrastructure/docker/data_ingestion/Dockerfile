ARG BASE_IMAGE=sfs_base:latest
FROM ${BASE_IMAGE}

WORKDIR /app/backend/services/data_ingestion
COPY backend/services/data_ingestion /app/backend/services/data_ingestion

RUN pip install --no-cache-dir fastapi uvicorn requests

EXPOSE 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
