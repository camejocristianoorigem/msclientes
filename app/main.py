from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.redis import init_redis, close_redis
from app.services.cliente_service import router as cliente_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_redis()
    yield
    await close_redis()

app = FastAPI(
    title="Microserviço de Clientes",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cliente_router, prefix="/clientes", tags=["Clientes"])

@app.get("/health", tags=["Healthcheck"])
async def health_check():
    return {"status": "ok"}
