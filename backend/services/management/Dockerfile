# backend/services/management/Dockerfile

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# برای psycopg2 و غیره
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# فرض می‌کنیم requirements.txt در همین پوشه هست
COPY requirements.txt /app/

RUN pip install --upgrade pip && pip install -r requirements.txt

# کد پروژه
COPY . /app/

EXPOSE 8000

CMD ["/bin/sh", "-c", "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]
