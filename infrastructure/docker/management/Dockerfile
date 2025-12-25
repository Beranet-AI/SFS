ARG BASE_IMAGE=sfs_base
FROM ${BASE_IMAGE}:latest

WORKDIR /app/backend/services/management

COPY backend/services/management .

RUN pip install --no-cache-dir \
    django \
    djangorestframework \
    django-extensions \
    psycopg2-binary

#CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
