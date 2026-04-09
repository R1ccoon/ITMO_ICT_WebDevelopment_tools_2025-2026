from datetime import datetime

from pydantic import BaseModel

from templates.enums import TransactionType


class CategoryCreateRequest(BaseModel):
    name: str
    direction: TransactionType


class CategoryModel(BaseModel):
    id: int
    user_id: int
    name: str
    direction: TransactionType
    is_system: bool
    d_create: datetime


class CategoryListResponse(BaseModel):
    data: list[CategoryModel]
