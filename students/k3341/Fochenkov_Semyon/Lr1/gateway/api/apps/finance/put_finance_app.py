from fastapi import APIRouter, Depends

from config import oauth2_scheme
from core.finance.put_finance_core import (
    update_account_implementation,
    update_budget_implementation,
    update_category_implementation,
    update_goal_implementation,
    update_tag_implementation,
    update_transaction_implementation,
)
from templates.base_models.finance_account import AccountModel
from templates.base_models.finance_budget import BudgetModel
from templates.base_models.finance_category import CategoryModel
from templates.base_models.finance_goal import GoalModel
from templates.base_models.finance_tag import TagModel
from templates.base_models.finance_transaction import TransactionModel
from templates.base_models.finance_update import (
    AccountUpdateRequest,
    BudgetUpdateRequest,
    CategoryUpdateRequest,
    GoalUpdateRequest,
    TagUpdateRequest,
    TransactionUpdateRequest,
)

put_finance_router = APIRouter()


@put_finance_router.put(
    "/accounts/{account_id}", response_model=AccountModel, description="Обновить счет"
)
async def update_account(
    account_id: int, data: AccountUpdateRequest, token: str = Depends(oauth2_scheme)
):
    return await update_account_implementation(
        account_id=account_id, data=data, token=token
    )


@put_finance_router.put(
    "/categories/{category_id}",
    response_model=CategoryModel,
    description="Обновить категорию",
)
async def update_category(
    category_id: int, data: CategoryUpdateRequest, token: str = Depends(oauth2_scheme)
):
    return await update_category_implementation(
        category_id=category_id, data=data, token=token
    )


@put_finance_router.put(
    "/transactions/{transaction_id}",
    response_model=TransactionModel,
    description="Обновить транзакцию",
)
async def update_transaction(
    transaction_id: int,
    data: TransactionUpdateRequest,
    token: str = Depends(oauth2_scheme),
):
    return await update_transaction_implementation(
        transaction_id=transaction_id, data=data, token=token
    )


@put_finance_router.put(
    "/budgets/{budget_id}", response_model=BudgetModel, description="Обновить бюджет"
)
async def update_budget(
    budget_id: int, data: BudgetUpdateRequest, token: str = Depends(oauth2_scheme)
):
    return await update_budget_implementation(
        budget_id=budget_id, data=data, token=token
    )


@put_finance_router.put(
    "/goals/{goal_id}", response_model=GoalModel, description="Обновить финансовую цель"
)
async def update_goal(
    goal_id: int, data: GoalUpdateRequest, token: str = Depends(oauth2_scheme)
):
    return await update_goal_implementation(goal_id=goal_id, data=data, token=token)


@put_finance_router.put(
    "/tags/{tag_id}", response_model=TagModel, description="Обновить тег"
)
async def update_tag(
    tag_id: int, data: TagUpdateRequest, token: str = Depends(oauth2_scheme)
):
    return await update_tag_implementation(tag_id=tag_id, data=data, token=token)
