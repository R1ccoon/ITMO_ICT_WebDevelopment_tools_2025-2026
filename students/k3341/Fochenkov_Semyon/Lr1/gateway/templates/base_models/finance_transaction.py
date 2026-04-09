from datetime import datetime

from pydantic import BaseModel, Field

from templates.enums import TransactionType


class TransactionTagModel(BaseModel):
    id: int
    name: str
    relevance_score: float


class TransactionCreateRequest(BaseModel):
    account_id: int
    category_id: int
    transaction_type: TransactionType
    amount: float
    note: str | None = None
    happened_at: datetime | None = None


class TransactionModel(BaseModel):
    id: int
    user_id: int
    account_id: int
    category_id: int
    transaction_type: TransactionType
    amount: float
    note: str | None
    happened_at: datetime
    d_create: datetime


class TransactionListResponse(BaseModel):
    data: list[TransactionModel]


class TransactionDetailsModel(TransactionModel):
    tags: list[TransactionTagModel] = Field(default_factory=list)
