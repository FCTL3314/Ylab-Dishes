from fastapi import Depends

from app.submenu.repository import SubmenuWithCountingRepository
from app.submenu.schemas import SubmenuResponse
from app.submenu.services import CachedSubmenuService, SubmenuService


def submenu_service() -> SubmenuService[SubmenuResponse]:
    return SubmenuService[SubmenuResponse](SubmenuWithCountingRepository())


ActiveSubmenuService = Depends(submenu_service)


def cached_submenu_service() -> CachedSubmenuService[SubmenuResponse]:
    return CachedSubmenuService[SubmenuResponse](SubmenuWithCountingRepository())


ActiveCachedSubmenuService = Depends(cached_submenu_service)
