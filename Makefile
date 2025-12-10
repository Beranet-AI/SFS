# ---------- Backend Quality Tools ----------
backend-format:
	black backend

backend-lint:
	pylint backend --exit-zero

backend-typecheck:
	mypy backend --ignore-missing-imports

backend-security:
	bandit -r backend

backend-check: backend-format backend-lint backend-typecheck backend-security


# ---------- Frontend ----------
frontend-lint:
	cd frontend/webapp && npm run lint

frontend-format:
	cd frontend/webapp && npm run format

frontend-check: frontend-lint frontend-format


# ---------- Full Project Check ----------
check: backend-check frontend-check
