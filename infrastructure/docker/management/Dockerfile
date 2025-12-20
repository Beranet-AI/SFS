#FROM python:3.11-slim

# 1. مسیر کاری = ریشه پروژه Django
#WORKDIR /app/management

# 2. کپی سورس‌ها
#COPY backend/services/management /app/management
#COPY backend/shared /app/shared

# 3. نصب وابستگی‌ها
#RUN pip install --no-cache-dir \
#    django \
#    djangorestframework \
#    django-extensions \
#    uvicorn \
#    psycopg2-binary \
#    requests

# 4. معرفی shared و management به Python
#ENV PYTHONPATH=/app

# 5. اجرای Django با ASGI صحیح
#CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0"]


FROM python:3.11-slim

WORKDIR /app

COPY backend/services/management /app
COPY backend/shared /app/shared

RUN pip install --no-cache-dir \
    django \
    djangorestframework \
    django-extensions \
    psycopg2-binary \
    uvicorn \
    requests \
    gunicorn \
    whitenoise

ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=config.settings.dev

CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
