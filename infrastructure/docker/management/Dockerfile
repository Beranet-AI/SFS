FROM python:3.11-slim

WORKDIR /app

COPY backend/services/management /app
COPY backend/shared /app/shared

RUN pip install --no-cache-dir \
    django \
    djangorestframework \
    psycopg2-binary \
    requests

ENV PYTHONPATH=/app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
