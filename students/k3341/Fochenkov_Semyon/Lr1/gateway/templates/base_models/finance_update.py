from datetime import datetime

from pydantic import BaseModel

from templates.enums import BudgetPeriod, GoalStatus, TransactionType


class AccountUpdateRequest(BaseModel):
    name: str | None = None
    currency_code: str | None = None
    balance: float | None = None
    is_archived: bool | None = None


class CategoryUpdateRequest(BaseModel):
    name: str | None = None
    direction: TransactionType | None = None


class TransactionUpdateRequest(BaseModel):
    account_id: int | None = None
    category_id: int | None = None
    transaction_type: TransactionType | None = None
    amount: float | None = None
    note: str | None = None
    happened_at: datetime | None = None


class BudgetUpdateRequest(BaseModel):
    category_id: int | None = None
    period: BudgetPeriod | None = None
    limit_amount: float | None = None
    spent_amount: float | None = None


class GoalUpdateRequest(BaseModel):
    name: str | None = None
    target_amount: float | None = None
    current_amount: float | None = None
    deadline: datetime | None = None
    status: GoalStatus | None = None


class TagUpdateRequest(BaseModel):
    name: str | None = None
