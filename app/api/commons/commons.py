from datetime import datetime, timezone
from uuid import uuid4


def get_current_datetime():
    return str(datetime.now(tz=timezone.utc))


def uuid() -> str:
    return str(uuid4())


def error_response(
    error: str, details: dict, message: str, path: str, status: int
) -> tuple:
    error = {
        "details": details,
        "error": error,
        "message": message,
        "path": path,
        "timestamp": str(datetime.now()),
        "status": status,
    }
    return error, status
