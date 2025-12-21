# =========================
# Base image (injected by docker-compose)
# =========================
ARG BASE_IMAGE=sfs_base
FROM ${BASE_IMAGE}:latest

# Keep a stable application root so shared/ and service code resolve cleanly
WORKDIR /app/backend/services/monitoring

# Copy service source code
COPY backend/services/monitoring /app/backend/services/monitoring

# Install service-specific dependencies
RUN pip install --no-cache-dir fastapi uvicorn requests

# Start service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]