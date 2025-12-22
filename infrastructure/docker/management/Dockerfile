ARG BASE_IMAGE=sfs_base:latest
FROM ${BASE_IMAGE}

WORKDIR /app/backend/services/management

# کپی سورس سرویس
COPY backend/services/management /app/backend/services/management

# وابستگی‌های این سرویس
RUN pip install --no-cache-dir \
    django \
    djangorestframework \
    django-extensions \
    psycopg2-binary \
    requests \
    gunicorn \
    uvicorn

# پیش‌فرض تنظیمات (اگر env_file گذاشتی، همان override می‌کند)
ENV DJANGO_SETTINGS_MODULE=config.settings.dev

EXPOSE 8000

# حالت DEV:
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
