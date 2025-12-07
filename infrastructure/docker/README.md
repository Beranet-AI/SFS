# Docker Assets

This folder is the canonical home for Docker Compose stacks and related artifacts. Use `docker-compose.yml` in this directory when bringing the stack up, for example:

```
docker compose -f infrastructure/docker/docker-compose.yml up --build
```

Environment variables are loaded from `infrastructure/.env.example` (or a local `infrastructure/.env` copy you create). Update `env_file` paths if you maintain a different location.
