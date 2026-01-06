#FROM sfs_base:latest

#WORKDIR /app

#COPY backend/services/edge_controller /app/backend/services/edge_controller

#RUN pip install --no-cache-dir fastapi uvicorn requests jsonschema scapy

#CMD ["uvicorn","backend.services.edge_controller.main:app","--host", "0.0.0.0","--port", "8003"]


FROM sfs_base:latest

WORKDIR /app

# کل backend را کپی کن، نه فقط یک سرویس
COPY backend /app/backend

# نصب وابستگی‌ها
RUN pip install --no-cache-dir fastapi uvicorn requests jsonschema scapy paho-mqtt

# اجرای uvicorn با app-dir درست
CMD ["uvicorn","services.edge_controller.main:app","--host", "0.0.0.0","--port", "8003","--app-dir", "/app/backend"]
