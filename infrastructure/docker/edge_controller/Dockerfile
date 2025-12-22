ARG BASE_IMAGE=sfs_base:latest
FROM ${BASE_IMAGE}

WORKDIR /app/backend/services/edge_controller
COPY backend/services/edge_controller /app/backend/services/edge_controller

RUN pip install --no-cache-dir fastapi uvicorn requests

EXPOSE 8003
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
