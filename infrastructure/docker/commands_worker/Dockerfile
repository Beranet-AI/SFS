FROM sfs_base:latest

WORKDIR /app/backend/services/management

ENV PYTHONUNBUFFERED=1

COPY backend/services/management /app/backend/services/management

RUN pip install --no-cache-dir \
    django \
    djangorestframework \
    psycopg2-binary \
    requests

CMD ["python", "-m", "apps.commands.application.workers.run_commands_worker"]
