from fastapi import HTTPException

from models.main_finance_account_model import Account
from models.main_finance_budget_model import Budget
from models.main_finance_category_model import Category
from models.main_finance_goal_model import FinancialGoal
from models.main_finance_transaction_model import Tag, Transaction
from templates.base_models.finance_account import AccountModel
from templates.base_models.finance_budget import BudgetModel
from templates.base_models.finance_category import CategoryModel
from templates.base_models.finance_goal import GoalModel
from templates.base_models.finance_tag import TagModel
from templates.base_models.finance_transaction import TransactionModel
from logs.log_worker import custom_core_decorator

from config import database_engine_async
from utils.internal_workers.auth_worker import AuthNamespace
from utils.internal_workers.database_worker import DatabaseWorkerAsync

database_worker = DatabaseWorkerAsync(database_engine_async)


async def get_current_user_id(token: str) -> int:
    user = await AuthNamespace.get_current_user(token=token)
    return user.id


@custom_core_decorator
async def update_account_implementation(account_id: int, data, token: str):
    user_id = await get_current_user_id(token)
    rows = await database_worker.custom_update(
        cls_to=Account,
        where_params=[Account.id == account_id, Account.user_id == user_id],
        data=data.model_dump(exclude_unset=True),
        returning=Account,
    )
    if not rows:
        raise HTTPException(status_code=404, detail="Account not found")
    return AccountModel(**rows[0].as_dict())


@custom_core_decorator
async def update_category_implementation(category_id: int, data, token: str):
    user_id = await get_current_user_id(token)
    rows = await database_worker.custom_update(
        cls_to=Category,
        where_params=[Category.id == category_id, Category.user_id == user_id],
        data=data.model_dump(exclude_unset=True),
        returning=Category,
    )
    if not rows:
        raise HTTPException(status_code=404, detail="Category not found")
    return CategoryModel(**rows[0].as_dict())


@custom_core_decorator
async def update_transaction_implementation(transaction_id: int, data, token: str):
    user_id = await get_current_user_id(token)
    rows = await database_worker.custom_update(
        cls_to=Transaction,
        where_params=[Transaction.id == transaction_id, Transaction.user_id == user_id],
        data=data.model_dump(exclude_unset=True),
        returning=Transaction,
    )
    if not rows:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return TransactionModel(**rows[0].as_dict())


@custom_core_decorator
async def update_budget_implementation(budget_id: int, data, token: str):
    user_id = await get_current_user_id(token)
    rows = await database_worker.custom_update(
        cls_to=Budget,
        where_params=[Budget.id == budget_id, Budget.user_id == user_id],
        data=data.model_dump(exclude_unset=True),
        returning=Budget,
    )
    if not rows:
        raise HTTPException(status_code=404, detail="Budget not found")
    return BudgetModel(**rows[0].as_dict())


@custom_core_decorator
async def update_goal_implementation(goal_id: int, data, token: str):
    user_id = await get_current_user_id(token)
    rows = await database_worker.custom_update(
        cls_to=FinancialGoal,
        where_params=[FinancialGoal.id == goal_id, FinancialGoal.user_id == user_id],
        data=data.model_dump(exclude_unset=True),
        returning=FinancialGoal,
    )
    if not rows:
        raise HTTPException(status_code=404, detail="Goal not found")
    return GoalModel(**rows[0].as_dict())


@custom_core_decorator
async def update_tag_implementation(tag_id: int, data, token: str):
    user_id = await get_current_user_id(token)
    rows = await database_worker.custom_update(
        cls_to=Tag,
        where_params=[Tag.id == tag_id, Tag.user_id == user_id],
        data=data.model_dump(exclude_unset=True),
        returning=Tag,
    )
    if not rows:
        raise HTTPException(status_code=404, detail="Tag not found")
    return TagModel(**rows[0].as_dict())
