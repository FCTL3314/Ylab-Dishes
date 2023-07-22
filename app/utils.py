from fastapi import HTTPException

from http import HTTPStatus


def get_object_or_404(model, identifier, session, not_found_msg="Object not found"):
    obj = session.get(model, identifier)
    if obj is None:
        raise HTTPException(detail=not_found_msg, status_code=HTTPStatus.NOT_FOUND)
    return obj
