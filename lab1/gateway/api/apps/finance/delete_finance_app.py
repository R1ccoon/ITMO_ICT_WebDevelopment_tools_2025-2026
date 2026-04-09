from fastapi import APIRouter, Depends

from config import oauth2_scheme
from core.finance.delete_finance_core import (
    delete_account_implementation,
    delete_budget_implementation,
    delete_category_implementation,
    delete_goal_implementation,
    delete_tag_implementation,
    delete_transaction_implementation,
)
from templates.base_models.finance_user import DefaultResponseModel

delete_finance_router = APIRouter()


@delete_finance_router.delete(
    "/accounts/{account_id}",
    response_model=DefaultResponseModel,
    description="Удалить счет",
)
async def delete_account(account_id: int, token: str = Depends(oauth2_scheme)):
    return await delete_account_implementation(account_id=account_id, token=token)


@delete_finance_router.delete(
    "/categories/{category_id}",
    response_model=DefaultResponseModel,
    description="Удалить категорию",
)
async def delete_category(category_id: int, token: str = Depends(oauth2_scheme)):
    return await delete_category_implementation(category_id=category_id, token=token)


@delete_finance_router.delete(
    "/transactions/{transaction_id}",
    response_model=DefaultResponseModel,
    description="Удалить транзакцию",
)
async def delete_transaction(transaction_id: int, token: str = Depends(oauth2_scheme)):
    return await delete_transaction_implementation(
        transaction_id=transaction_id, token=token
    )


@delete_finance_router.delete(
    "/budgets/{budget_id}",
    response_model=DefaultResponseModel,
    description="Удалить бюджет",
)
async def delete_budget(budget_id: int, token: str = Depends(oauth2_scheme)):
    return await delete_budget_implementation(budget_id=budget_id, token=token)


@delete_finance_router.delete(
    "/goals/{goal_id}",
    response_model=DefaultResponseModel,
    description="Удалить финансовую цель",
)
async def delete_goal(goal_id: int, token: str = Depends(oauth2_scheme)):
    return await delete_goal_implementation(goal_id=goal_id, token=token)


@delete_finance_router.delete(
    "/tags/{tag_id}", response_model=DefaultResponseModel, description="Удалить тег"
)
async def delete_tag(tag_id: int, token: str = Depends(oauth2_scheme)):
    return await delete_tag_implementation(tag_id=tag_id, token=token)
