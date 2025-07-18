from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import logger, settings
from app.enums import LIFESPAN_STARTED
from app.routers.api import router


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info(LIFESPAN_STARTED)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url=f"{settings.APP_PATH}/docs",
    redoc_url=f"{settings.APP_PATH}/redoc",
    openapi_url=f"{settings.APP_PATH}/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.APP_PATH)
