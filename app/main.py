from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  #(registra os models no Base)
from app.database import Base, engine
from app.routes import router
from app.logging_config import configurar_logging

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.limiter import limiter

from pathlib import Path

from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

configurar_logging()

app = FastAPI(title="Consulta de CEP", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.include_router(router, prefix="/api")

@app.middleware("http")
async def adicionar_headers_seguranca(request, call_next):
    resposta = await call_next(request)
    resposta.headers["X-Content-Type-Options"] = "nosniff"
    resposta.headers["X-Frame-Options"] = "DENY"
    resposta.headers["Referrer-Policy"] = "no-referrer"
    if not request.url.path.startswith(("/docs", "/redoc", "/openapi.json")):
        resposta.headers["Content-Security-Policy"] = (
            "default-src 'self'; frame-ancestors 'none'"
        )
    return resposta


FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"

if FRONTEND_DIST.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")

@app.get("/health")
def health():
    return {"status": "ok"}