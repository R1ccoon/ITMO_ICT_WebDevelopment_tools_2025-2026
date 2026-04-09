from fastapi import APIRouter, Depends

from config import oauth2_scheme
from core.finance.get_finance_core import (
    list_accounts_implementation,
    list_budgets_implementation,
    list_categories_implementation,
    list_goals_implementation,
    list_tags_implementation,
    list_transactions_implementation,
)
from templates.base_models.finance_account import AccountListResponse
from templates.base_models.finance_budget import BudgetListResponse
from templates.base_models.finance_category import CategoryListResponse
from templates.base_models.finance_goal import GoalListResponse
from templates.base_models.finance_tag import TagListResponse
from templates.base_models.finance_transaction import TransactionListResponse

get_finance_router = APIRouter()


@get_finance_router.get(
    "/accounts",
    response_model=AccountListResponse,
    description="Получить список счетов пользователя",
)
async def list_accounts(token: str = Depends(oauth2_scheme)):
    return await list_accounts_implementation(token=token)


@get_finance_router.get(
    "/categories",
    response_model=CategoryListResponse,
    description="Получить список категорий пользователя",
)
async def list_categories(token: str = Depends(oauth2_scheme)):
    return await list_categories_implementation(token=token)


@get_finance_router.get(
    "/transactions",
    response_model=TransactionListResponse,
    description="Получить список транзакций пользователя",
)
async def list_transactions(token: str = Depends(oauth2_scheme)):
    return await list_transactions_implementation(token=token)


@get_finance_router.get(
    "/budgets",
    response_model=BudgetListResponse,
    description="Получить список бюджетов пользователя",
)
async def list_budgets(token: str = Depends(oauth2_scheme)):
    return await list_budgets_implementation(token=token)


@get_finance_router.get(
    "/goals",
    response_model=GoalListResponse,
    description="Получить список финансовых целей пользователя",
)
async def list_goals(token: str = Depends(oauth2_scheme)):
    return await list_goals_implementation(token=token)


@get_finance_router.get(
    "/tags",
    response_model=TagListResponse,
    description="Получить список тегов пользователя",
)
async def list_tags(token: str = Depends(oauth2_scheme)):
    return await list_tags_implementation(token=token)
