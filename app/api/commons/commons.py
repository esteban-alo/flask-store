from datetime import datetime
from uuid import uuid4


def uuid() -> str:
    return str(uuid4())


def error_response(error: str, details: dict, message: str, path: str, status: int) -> tuple:
    error = {
        "details": details,
        "error": error,
        "message": message,
        "path": path,
        "timestamp": datetime.now().__str__(),
        "status": status
    }
    return error, status
