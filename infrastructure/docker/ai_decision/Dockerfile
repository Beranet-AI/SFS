ARG BASE_IMAGE=sfs_base:latest
FROM ${BASE_IMAGE}

WORKDIR /app/backend/services/ai_decision
COPY backend/services/ai_decision /app/backend/services/ai_decision

RUN pip install --no-cache-dir fastapi uvicorn requests

EXPOSE 8004
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8004"]
