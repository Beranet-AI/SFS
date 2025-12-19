from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    # startup (load ML models)
    yield
    # shutdown
