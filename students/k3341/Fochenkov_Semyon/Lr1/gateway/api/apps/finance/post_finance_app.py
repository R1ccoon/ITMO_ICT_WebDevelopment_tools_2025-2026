from fastapi import APIRouter, Depends

from config import oauth2_scheme
from core.finance.post_finance_core import (
    bind_tag_implementation,
    create_account_implementation,
    create_budget_implementation,
    create_category_implementation,
    create_goal_implementation,
    create_tag_implementation,
    create_transaction_implementation,
)
from templates.base_models.finance_account import AccountCreateRequest
from templates.base_models.finance_account import AccountModel
from templates.base_models.finance_budget import BudgetCreateRequest
from templates.base_models.finance_budget import BudgetModel
from templates.base_models.finance_category import CategoryCreateRequest
from templates.base_models.finance_category import CategoryModel
from templates.base_models.finance_goal import GoalCreateRequest
from templates.base_models.finance_goal import GoalModel
from templates.base_models.finance_tag import (
    TagCreateRequest,
    TagModel,
    TransactionTagBindRequest,
)
from templates.base_models.finance_transaction import (
    TransactionCreateRequest,
    TransactionModel,
)
from templates.base_models.finance_user import DefaultResponseModel

post_finance_router = APIRouter()


@post_finance_router.post(
    "/accounts", response_model=AccountModel, description="Создать новый счет"
)
async def create_account(
    data: AccountCreateRequest, token: str = Depends(oauth2_scheme)
):
    return await create_account_implementation(data=data, token=token)


@post_finance_router.post(
    "/categories", response_model=CategoryModel, description="Создать новую категорию"
)
async def create_category(
    data: CategoryCreateRequest, token: str = Depends(oauth2_scheme)
):
    return await create_category_implementation(data=data, token=token)


@post_finance_router.post(
    "/transactions",
    response_model=TransactionModel,
    description="Создать новую транзакцию",
)
async def create_transaction(
    data: TransactionCreateRequest, token: str = Depends(oauth2_scheme)
):
    return await create_transaction_implementation(data=data, token=token)


@post_finance_router.post(
    "/budgets", response_model=BudgetModel, description="Создать бюджет"
)
async def create_budget(data: BudgetCreateRequest, token: str = Depends(oauth2_scheme)):
    return await create_budget_implementation(data=data, token=token)


@post_finance_router.post(
    "/goals", response_model=GoalModel, description="Создать финансовую цель"
)
async def create_goal(data: GoalCreateRequest, token: str = Depends(oauth2_scheme)):
    return await create_goal_implementation(data=data, token=token)


@post_finance_router.post("/tags", response_model=TagModel, description="Создать тег")
async def create_tag(data: TagCreateRequest, token: str = Depends(oauth2_scheme)):
    return await create_tag_implementation(data=data, token=token)


@post_finance_router.post(
    "/transaction-tags",
    response_model=DefaultResponseModel,
    description="Привязать тег к транзакции",
)
async def bind_tag(
    data: TransactionTagBindRequest, token: str = Depends(oauth2_scheme)
):
    return await bind_tag_implementation(data=data, token=token)
