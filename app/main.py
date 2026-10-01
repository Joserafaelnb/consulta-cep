from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  #(registra os models no Base)
from app.database import Base, engine
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Consulta de CEP", lifespan=lifespan)
app.include_router(router)
    

@app.get("/health")
def health():
    return {"status": "ok"}