from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    # startup hooks (connect mqtt, etc.)
    yield
    # shutdown hooks
