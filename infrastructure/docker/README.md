# Docker Assets

This folder is the canonical home for Docker Compose stacks and related artifacts. Use `docker-compose.yml` in this directory when bringing the stack up, for example:

```
docker compose -f infrastructure/docker/docker-compose.yml up --build
```

Environment files are still expected one level up under `infra/.env.global` (or you can create a local copy alongside this file by adjusting the `env_file` paths).
