from fastapi import Depends

from app.db import get_async_session

ActiveSession = Depends(get_async_session)
