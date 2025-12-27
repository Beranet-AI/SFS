FROM sfs_base:latest

WORKDIR /app

COPY backend/services/ai_decision /app/backend/services/ai_decision

RUN pip install --no-cache-dir fastapi uvicorn requests

CMD ["uvicorn","backend.services.ai_decision.main:app","--host", "0.0.0.0","--port", "8004"]
