from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import router
from .config import settings
from .db import SessionLocal
from .service import seed_defaults


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.imp_bootstrap_defaults:
        with SessionLocal() as db:
            seed_defaults(db)
    yield


app = FastAPI(title="IMP API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
