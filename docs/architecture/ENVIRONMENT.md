This document standardizes how environment variables are managed and structured across the project. It defines naming conventions, file locations, integration with Docker Compose, and best practices for configuration in each service.

1. Global Rules

.env files must not be committed to version control (Git).
Every .env must have a corresponding .env.example file with the same keys and empty/sample values.
Each service must load its configuration through a centralized config module:
config/settings.py for Django
config.py for FastAPI
Environment variables should never be hard-coded directly in the codebase.

2. File Structure by Service
    
    Root (optional for development):
        .env

    Django – Management:
        backend/services/management/
        ├── .env
        ├── .env.docker
        └── .env.example

    FastAPI – data_ingestion:
        backend/services/data_ingestion/
        ├── .env
        ├── .env.docker
        └── .env.example

    FastAPI – ai_decision:
        backend/services/ai_decision/
        ├── .env
        ├── .env.docker
        └── .env.example

    FastAPI – Monitoring:
        backend/services/monitoring/
        ├── .env
        ├── .env.docker
        └── .env.example

    Next.js - Webapp:
        frontend/webapp/
        ├── .env.local
        └── .env.example

    React Native - Mobileapp:
        frontend/mobileapp/
        ├── .env.local
        └── .env.example

3. Environment Variable Naming Conventions

    Django (management)

        | Variable Name          | Example                           | Description                                          |
        | ---------------------- | --------------------------------- | -----------------------------------------------------|
        | `DJANGO_SECRET_KEY`    | `supersecretkey`                  | Django secret key for cryptographic ops              |
        | `DJANGO_DEBUG`         | `True` / `False`                  | Enable/disable debug mode                            |
        | `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1`             | Allowed hostnames                                    |
        | `DJANGO_DATABASE_URL`  | `postgres://user:pass@db:5432/db` | PostgreSQL connection URL                            |
        | `SERVICE_AUTH_TOKEN`   | `internal-token-value`            | Token to authenticate incoming internal API requests |

    FastAPI (data_ingestion)

        | Variable Name             | Example                         | Description                            |
        | ------------------------- | ------------------------------- | -------------------------------------- |
        | `DJANGO_API_BASE_URL`     | `http://management:8000/api/v1` | Django backend base URL                |
        | `DJANGO_SERVICE_USERNAME` | `fastapi_service`               | Service account username for Django    |
        | `DJANGO_SERVICE_PASSWORD` | `securepassword`                | Password for service authentication    |
        | `SERVICE_AUTH_TOKEN`      | `internal-token-value`          | Internal token for FastAPI→Django auth |

    FastAPI (monitoring)

        | Variable Name          | Example                     | Description                                        |
        | ---------------------- | --------------------------- | -------------------------------------------------- |
        | `ALERT_RULES_PATH`     | `./data/alert_rules.yaml`   | Path to live-status rule configuration (if used)   |
        | `NOTIFICATION_ENABLED` | `True`                      | Whether notifications are enabled                  |
        | `LOG_ALERTS`           | `True`                      | Whether to log triggered live status to console    |

    FastAPI (ai_decision)

        | Variable Name             | Example                       | Description                              |
        | ------------------------- | ----------------------------- | ---------------------------------------- |
        | `MODEL_PATH`              | `./models/decision_model.pkl` | Path to saved ML model                   |
        | `DECISION_THRESHOLD`      | `0.75`                        | Threshold for binary decisioning         |
        | `SERVICE_AUTH_TOKEN`      | `internal-token`              | Token for API authorization              |
        | `DJANGO_API_BASE_URL`     | `http://django:8000/api/v1/`  | Base URL of Django backend               |
        | `DJANGO_SERVICE_USERNAME` | `fastapi_service`             | Django internal service username         |
        | `DJANGO_SERVICE_PASSWORD` | `securepassword`              | Django internal service password         |
        | `LOG_LEVEL`               | `INFO`                        | Logging level (`DEBUG`, `INFO`, `ERROR`) |
        | `SERVICE_PORT`            | `8000`                        | Port to expose FastAPI service           |

    FastAPI (edge_controller)

        | Variable Name        | Example                      | Description                                           |
        | -------------------- | ---------------------------- | ----------------------------------------------------- |
        | `SERVICE_PORT`       | `8000`                       | Port to expose FastAPI service                        |
        | `SERVICE_AUTH_TOKEN` | `internal-token`             | Shared token used for internal service authentication |
        | `MQTT_BROKER_URL`    | `mqtt://mqtt:1883`           | MQTT broker address for sensor data ingestion         |
        | `CENTRAL_API_URL`    | `http://django:8000/api/v1/` | Django API URL to post data to central server         |
        | `DEVICE_ID`          | `edge-001`                   | Optional ID of edge device instance                   |

    Next.js (webapp)

        | Variable Name                     | Example                        | Description                                          |
        | --------------------------------- | ------------------------------ | ---------------------------------------------------- |
        | `NEXT_PUBLIC_DJANGO_API_BASE_URL` | `http://localhost:8000/api/v1` | Base URL for Django API                              |
        | `NEXT_PUBLIC_FASTAPI_BASE_URL`    | `http://localhost:9000`        | Base URL for FastAPI                                 |
        | `NEXT_PUBLIC_FASTAPI_TOKEN`       | `internal-token-value`         | Token used by the frontend to authenticate with APIs |
        | `NEXT_PUBLIC_SENSOR_TYPES`        | `temperature,ammonia`          | Comma-separated list of sensor types to track        |
        | `NEXT_PUBLIC_API_PREFIX`          | `api/v1`                       | API prefix for dynamic endpoint construction         |


    React Native (mobileapp)

        | Variable Name            | Example                            | Description                            |
        | ------------------------ | ---------------------------------- | -------------------------------------- |
        | `API_BASE_URL`           | `https://api.smartfarm.ir/api/v1/` | Base URL to connect to backend API     |
        | `AUTH_TOKEN_STORAGE_KEY` | `@smartfarm/token`                 | AsyncStorage key for saving auth token |
        | `ENABLE_LOGGING`         | `true`                             | Toggle for internal app debug logs     |


4. Docker Compose Integration

Each service's container must reference its Docker-specific .env.docker file to ensure proper configuration during builds and runtime.

backend:
    services:
        management:
            build:
            context: ./backend/services/management
            env_file: ./backend/services/management/.env.docker

        data_ingestion:
            build:
            context: ./backend/services/data_ingestion
            env_file: ./backend/services/data_ingestion/.env.docker

        ai_decision:
            build:
            context: ./backend/services/ai_decision
            env_file: ./backend/services/ai_decision/.env.docker

        monitoring:
            build:
            context: ./backend/services/monitoring
            env_file: ./backend/services/monitoring/.env.docker

edge:
    edge_controller:
        build:
        context: ./edge/edge_controller
        env_file: ./edge/edge_controller/.env.docker

frontend:
    webapp:
        build:
        context: ./frontend/webapp
        env_file: ./frontend/webapp/.env.local

    mobileapp:
        build:
        context: ./frontend/mobileapp
        env_file: ./frontend/mobileapp/.env.local

5. Additional Notes

    The SERVICE_AUTH_TOKEN must be consistent across services that communicate internally (FastAPI → Django).
    For environments like staging/production, define .env.staging, .env.prod, and set up .env.docker to load dynamically depending on the compose target.
    Use dotenv-linter or similar tools to validate .env files in CI pipelines.
