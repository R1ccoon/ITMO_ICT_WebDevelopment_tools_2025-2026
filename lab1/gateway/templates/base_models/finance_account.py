from datetime import datetime

from pydantic import BaseModel


class AccountCreateRequest(BaseModel):
    name: str
    currency_code: str
    balance: float = 0.0


class AccountModel(BaseModel):
    id: int
    user_id: int
    name: str
    currency_code: str
    balance: float
    is_archived: bool
    d_create: datetime


class AccountListResponse(BaseModel):
    data: list[AccountModel]
