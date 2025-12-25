FROM sfs_base:latest

# ریشه اجرای سرویس
WORKDIR /app

# کپی کل پکیج سرویس با نام خودش
COPY backend/services/edge_controller /app/edge_controller

# نصب وابستگی‌های runtime
RUN pip install --no-cache-dir fastapi uvicorn

# اجرای سرویس
CMD ["uvicorn", "edge_controller.main:app", "--host", "0.0.0.0", "--port", "8001"]
