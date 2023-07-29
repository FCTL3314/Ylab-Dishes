from http import HTTPStatus

from fastapi import HTTPException


async def get_first_or_404(query, session, not_found_msg="Object not found"):
    """
    Get object if it exists, otherwise raise HTTPException
    with status code 404.
    """
    result = await session.execute(query)
    obj = result.first()
    if obj is None:
        raise HTTPException(detail=not_found_msg, status_code=HTTPStatus.NOT_FOUND)
    return obj
