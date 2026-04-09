from models.main_finance_account_model import Account
from models.main_finance_budget_model import Budget
from models.main_finance_category_model import Category
from models.main_finance_goal_model import FinancialGoal
from models.main_finance_transaction_model import Tag, Transaction
from templates.base_models.finance_account import AccountListResponse, AccountModel
from templates.base_models.finance_budget import BudgetListResponse, BudgetModel
from templates.base_models.finance_category import CategoryListResponse, CategoryModel
from templates.base_models.finance_goal import GoalListResponse, GoalModel
from templates.base_models.finance_tag import TagListResponse, TagModel
from templates.base_models.finance_transaction import (
    TransactionListResponse,
    TransactionModel,
)
from logs.log_worker import custom_core_decorator

from config import database_engine_async
from utils.internal_workers.auth_worker import AuthNamespace
from utils.internal_workers.database_worker import DatabaseWorkerAsync

database_worker = DatabaseWorkerAsync(database_engine_async)


async def get_current_user_id(token: str) -> int:
    user = await AuthNamespace.get_current_user(token=token)
    return user.id


@custom_core_decorator
async def list_accounts_implementation(token: str):
    user_id = await get_current_user_id(token)
    rows = await database_worker.custom_orm_select(
        cls_from=Account,
        where_params=[Account.user_id == user_id],
        order_by=[Account.id.asc()],
    )
    return AccountListResponse(data=[AccountModel(**row.as_dict()) for row in rows])


@custom_core_decorator
async def list_categories_implementation(token: str):
    user_id = await get_current_user_id(token)
    rows = await database_worker.custom_orm_select(
        cls_from=Category,
        where_params=[Category.user_id == user_id],
        order_by=[Category.id.asc()],
    )
    return CategoryListResponse(data=[CategoryModel(**row.as_dict()) for row in rows])


@custom_core_decorator
async def list_transactions_implementation(token: str):
    user_id = await get_current_user_id(token)
    rows = await database_worker.custom_orm_select(
        cls_from=Transaction,
        where_params=[Transaction.user_id == user_id],
        order_by=[Transaction.id.asc()],
    )
    return TransactionListResponse(
        data=[TransactionModel(**row.as_dict()) for row in rows]
    )


@custom_core_decorator
async def list_budgets_implementation(token: str):
    user_id = await get_current_user_id(token)
    rows = await database_worker.custom_orm_select(
        cls_from=Budget,
        where_params=[Budget.user_id == user_id],
        order_by=[Budget.id.asc()],
    )
    return BudgetListResponse(data=[BudgetModel(**row.as_dict()) for row in rows])


@custom_core_decorator
async def list_goals_implementation(token: str):
    user_id = await get_current_user_id(token)
    rows = await database_worker.custom_orm_select(
        cls_from=FinancialGoal,
        where_params=[FinancialGoal.user_id == user_id],
        order_by=[FinancialGoal.id.asc()],
    )
    return GoalListResponse(data=[GoalModel(**row.as_dict()) for row in rows])


@custom_core_decorator
async def list_tags_implementation(token: str):
    user_id = await get_current_user_id(token)
    rows = await database_worker.custom_orm_select(
        cls_from=Tag, where_params=[Tag.user_id == user_id], order_by=[Tag.id.asc()]
    )
    return TagListResponse(data=[TagModel(**row.as_dict()) for row in rows])
