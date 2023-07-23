from fastapi import Depends

from app.db import get_session

ActiveSession = Depends(get_session)
