# =========================
# Base image (injected by docker-compose)
# =========================
ARG BASE_IMAGE=sfs_base
FROM ${BASE_IMAGE}:latest

ENV PYTHONPATH=/app/backend/services

# Keep a stable application root so shared/ and service code resolve cleanly
WORKDIR /app/backend/services/data_ingestion

# Copy service source code
COPY backend/services/data_ingestion /app/backend/services/data_ingestion

# Install service-specific dependencies
RUN pip install --no-cache-dir fastapi uvicorn requests

# Start service
CMD ["uvicorn", "data_ingestion.main:app", "--host", "0.0.0.0", "--port", "8001"]