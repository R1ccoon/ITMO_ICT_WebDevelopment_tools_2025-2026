from api.apps import router as apps_router
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(apps_router, tags=["App endpoints"])
