from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import schemas, services
from .database import Base, engine, get_db
from .routes.logs import router as logs_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Log Analyzer",
    version="1.0.0",
    description="A lightweight API for collecting, classifying and analyzing application logs.",
)

app.include_router(logs_router)


@app.get("/")
def root():
    return {
        "name": "Smart Log Analyzer",
        "docs": "/docs",
    }


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}


@app.get("/stats", response_model=schemas.StatsResponse, tags=["analytics"])
def stats(db: Session = Depends(get_db)):
    return services.build_stats(db)
