from fastapi import APIRouter

from api.apps.auth._auth_router import auth_router
from api.apps.finance._finance_router import finance_router
from api.apps.users._users_router import users_router


router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(users_router, tags=["Users"])
router.include_router(finance_router, tags=["Finance"])
