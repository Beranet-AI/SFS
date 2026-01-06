from contextlib import asynccontextmanager

from .logging import get_logger


logger = get_logger("lifespan")

@asynccontextmanager
async def lifespan(app):
    logger.info("Edge controller starting")
    yield
    logger.info("Edge controller stopping")
