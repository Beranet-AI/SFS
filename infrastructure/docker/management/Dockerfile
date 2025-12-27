
FROM sfs_base:latest

WORKDIR /app

# کپی سورس سرویس
COPY backend/services/management /app/backend/services/management

# نصب وابستگی‌ها
RUN pip install --no-cache-dir \
    django \
    djangorestframework \
    django-extensions \
    psycopg2-binary \
    httpx \
    requests

# اجرای Django
CMD ["python", "backend/services/management/manage.py", "runserver", "0.0.0.0:8000"]
