FROM sfs_base:latest

WORKDIR /app

COPY backend/services/edge_controller /app/backend/services/edge_controller

RUN pip install --no-cache-dir fastapi uvicorn requests

CMD ["uvicorn","backend.services.edge_controller.main:app","--host", "0.0.0.0","--port", "8003"]
