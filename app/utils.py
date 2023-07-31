from http import HTTPStatus

from fastapi import HTTPException


def is_obj_exists_or_404(obj, message):
    if not obj:
        raise HTTPException(detail=message, status_code=HTTPStatus.NOT_FOUND)
