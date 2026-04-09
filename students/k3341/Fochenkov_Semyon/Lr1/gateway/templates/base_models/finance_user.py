from datetime import datetime

from pydantic import BaseModel, EmailStr

from templates.base_models.finance_account import AccountModel
from templates.base_models.finance_budget import BudgetModel
from templates.base_models.finance_category import CategoryModel
from templates.base_models.finance_goal import GoalModel
from templates.base_models.finance_transaction import TransactionDetailsModel


class FinanceUserCreateRequest(BaseModel):
    email: EmailStr
    full_name: str
    password: str


class RegisterRequestModel(FinanceUserCreateRequest):
    pass


class FinanceLoginRequest(BaseModel):
    email: EmailStr
    password: str


class FinanceChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


class FinanceAuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class DefaultResponseModel(BaseModel):
    status: str
    detail: str


class ValidateBotTokenRequestModel(BaseModel):
    telegram_id: int
    validation_token: str


class FinanceUserModel(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool
    d_create: datetime


class FinanceUserListResponse(BaseModel):
    total_count: int
    users: list[FinanceUserModel]


class FinanceUserDetailsResponse(BaseModel):
    user: FinanceUserModel
    accounts: list[AccountModel]
    categories: list[CategoryModel]
    budgets: list[BudgetModel]
    goals: list[GoalModel]
    transactions: list[TransactionDetailsModel]
