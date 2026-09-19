from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

LogLevel = Literal["INFO", "WARNING", "ERROR"]


class LogCreate(BaseModel):
    message: str = Field(min_length=1, max_length=5000)
    source: str = Field(default="unknown", min_length=1, max_length=100)
    level: LogLevel | None = None


class LogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    message: str
    level: LogLevel
    source: str
    created_at: datetime


class StatsResponse(BaseModel):
    total: int
    info: int
    warning: int
    error: int
    top_messages: list[dict[str, int | str]]
