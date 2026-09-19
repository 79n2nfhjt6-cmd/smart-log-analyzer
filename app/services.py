import re
from collections import Counter

from sqlalchemy.orm import Session

from . import models


ERROR_WORDS = (
    "error", "exception", "failed", "failure", "fatal", "crash",
    "traceback", "timeout", "denied", "unavailable",
)
WARNING_WORDS = (
    "warning", "warn", "retry", "slow", "deprecated", "missing",
    "high latency", "rate limit",
)


def detect_level(message: str) -> str:
    text = message.lower()
    if any(word in text for word in ERROR_WORDS):
        return "ERROR"
    if any(word in text for word in WARNING_WORDS):
        return "WARNING"
    return "INFO"


def normalize_message(message: str) -> str:
    value = re.sub(r"\b\d+\b", "<n>", message.strip())
    value = re.sub(r"\s+", " ", value)
    return value[:160]


def build_stats(db: Session) -> dict:
    logs = db.query(models.LogEntry).all()
    counts = Counter(log.level for log in logs)
    common = Counter(normalize_message(log.message) for log in logs).most_common(5)

    return {
        "total": len(logs),
        "info": counts["INFO"],
        "warning": counts["WARNING"],
        "error": counts["ERROR"],
        "top_messages": [
            {"message": message, "count": count}
            for message, count in common
        ],
    }
