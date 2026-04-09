from datetime import datetime

from pydantic import BaseModel

from templates.enums import BudgetPeriod


class BudgetCreateRequest(BaseModel):
    category_id: int
    period: BudgetPeriod
    limit_amount: float


class BudgetModel(BaseModel):
    id: int
    user_id: int
    category_id: int
    period: BudgetPeriod
    limit_amount: float
    spent_amount: float
    d_create: datetime


class BudgetListResponse(BaseModel):
    data: list[BudgetModel]
