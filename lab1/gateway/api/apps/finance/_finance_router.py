from fastapi import APIRouter

from api.apps.finance.delete_finance_app import delete_finance_router
from api.apps.finance.get_finance_app import get_finance_router
from api.apps.finance.post_finance_app import post_finance_router
from api.apps.finance.put_finance_app import put_finance_router

finance_router = APIRouter()
finance_router.include_router(get_finance_router)
finance_router.include_router(post_finance_router)
finance_router.include_router(put_finance_router)
finance_router.include_router(delete_finance_router)
