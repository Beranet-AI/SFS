FROM sfs_base:latest

# ریشه اجرای سرویس
WORKDIR /app

# کپی کل پکیج سرویس با نام خودش
COPY backend/services/data_ingestion /app/data_ingestion

# نصب وابستگی‌های runtime
RUN pip install --no-cache-dir fastapi uvicorn

# اجرای سرویس
CMD ["uvicorn", "data_ingestion.main:app", "--host", "0.0.0.0", "--port", "8001"]
