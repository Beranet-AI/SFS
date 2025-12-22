ARG BASE_IMAGE=sfs_base:latest
FROM ${BASE_IMAGE}

WORKDIR /app/backend/services/monitoring
COPY backend/services/monitoring /app/backend/services/monitoring

RUN pip install --no-cache-dir fastapi uvicorn requests

EXPOSE 8002
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
