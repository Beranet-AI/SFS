$composeFile = "infrastructure/docker/docker-compose.yml"

Write-Host "▶ Migrating users..."
docker compose -f $composeFile exec management `
python backend/services/management/manage.py migrate users

Write-Host "▶ Migrating farms..."
docker compose -f $composeFile exec management `
python backend/services/management/manage.py migrate farms

Write-Host "▶ Migrating devices..."
docker compose -f $composeFile exec management `
python backend/services/management/manage.py migrate devices

Write-Host "▶ Migrating livestock..."
docker compose -f $composeFile exec management `
python backend/services/management/manage.py migrate livestock

Write-Host "▶ Migrating telemetry..."
docker compose -f $composeFile exec management `
python backend/services/management/manage.py migrate telemetry

Write-Host "▶ Migrating health..."
docker compose -f $composeFile exec management `
python backend/services/management/manage.py migrate health

Write-Host "✅ All migrations applied successfully."
