FROM sfs_base:latest

# ریشه اجرای سرویس
WORKDIR /app

# کپی کل پکیج سرویس با نام خودش
COPY backend/services/ai_decision /app/ai_decision

# نصب وابستگی‌های runtime
RUN pip install --no-cache-dir fastapi uvicorn

# اجرای سرویس
CMD ["uvicorn", "ai_decision.main:app", "--host", "0.0.0.0", "--port", "8001"]
