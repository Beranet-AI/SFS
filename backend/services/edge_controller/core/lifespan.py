from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    # startup
    yield
    # shutdown
