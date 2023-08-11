from http import HTTPStatus
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.engine import Row
from sqlmodel import SQLModel


def is_obj_exists_or_404(obj: SQLModel | Row | None, message: str) -> None:
    if not obj:
        raise HTTPException(detail=message, status_code=HTTPStatus.NOT_FOUND)


def is_valid_uuid(uuid: str) -> bool:
    try:
        UUID(uuid)
        return True
    except (ValueError, TypeError):
        return False
