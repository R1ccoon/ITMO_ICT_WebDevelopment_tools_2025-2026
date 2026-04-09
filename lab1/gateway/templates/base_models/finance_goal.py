from datetime import datetime

from pydantic import BaseModel

from templates.enums import GoalStatus


class GoalCreateRequest(BaseModel):
    name: str
    target_amount: float
    deadline: datetime | None = None


class GoalModel(BaseModel):
    id: int
    user_id: int
    name: str
    target_amount: float
    current_amount: float
    deadline: datetime | None
    status: GoalStatus
    d_create: datetime


class GoalListResponse(BaseModel):
    data: list[GoalModel]
