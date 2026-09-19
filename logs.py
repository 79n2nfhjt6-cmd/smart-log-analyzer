from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from .. import models, schemas, services
from ..database import get_db

router = APIRouter(prefix="/logs", tags=["logs"])


@router.post("", response_model=schemas.LogRead, status_code=status.HTTP_201_CREATED)
def create_log(payload: schemas.LogCreate, db: Session = Depends(get_db)):
    level = payload.level or services.detect_level(payload.message)
    log = models.LogEntry(
        message=payload.message,
        source=payload.source,
        level=level,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.get("", response_model=list[schemas.LogRead])
def list_logs(
    level: schemas.LogLevel | None = None,
    source: str | None = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    query = db.query(models.LogEntry)

    if level:
        query = query.filter(models.LogEntry.level == level)
    if source:
        query = query.filter(models.LogEntry.source == source)

    return (
        query.order_by(models.LogEntry.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
