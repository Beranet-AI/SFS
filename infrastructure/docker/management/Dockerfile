# =========================
# Base image (injected by docker-compose)
# =========================
ARG BASE_IMAGE=sfs_base
FROM ${BASE_IMAGE}:latest

# Stable working directory
WORKDIR /app/backend/services/management

# Copy Django service source
COPY backend/services/management /app/backend/services/management

# Install service-specific dependencies
RUN pip install --no-cache-dir \
    django \
    djangorestframework \
    psycopg2-binary \
    django-extensions \
    requests

# Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
