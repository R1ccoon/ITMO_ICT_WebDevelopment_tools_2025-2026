from models.main_finance_account_model import Account
from models.main_finance_budget_model import Budget
from models.main_finance_category_model import Category
from models.main_finance_goal_model import FinancialGoal
from models.main_finance_transaction_model import Tag, Transaction
from templates.base_models.finance_user import DefaultResponseModel
from logs.log_worker import custom_core_decorator

from config import database_engine_async
from utils.internal_workers.auth_worker import AuthNamespace
from utils.internal_workers.database_worker import DatabaseWorkerAsync

database_worker = DatabaseWorkerAsync(database_engine_async)


async def get_current_user_id(token: str) -> int:
    user = await AuthNamespace.get_current_user(token=token)
    return user.id


@custom_core_decorator
async def delete_account_implementation(account_id: int, token: str):
    user_id = await get_current_user_id(token)
    await database_worker.custom_delete_all(
        cls_from=Account,
        where_params=[Account.id == account_id, Account.user_id == user_id],
    )
    return DefaultResponseModel(status="success", detail="Account deleted")


@custom_core_decorator
async def delete_category_implementation(category_id: int, token: str):
    user_id = await get_current_user_id(token)
    await database_worker.custom_delete_all(
        cls_from=Category,
        where_params=[Category.id == category_id, Category.user_id == user_id],
    )
    return DefaultResponseModel(status="success", detail="Category deleted")


@custom_core_decorator
async def delete_transaction_implementation(transaction_id: int, token: str):
    user_id = await get_current_user_id(token)
    await database_worker.custom_delete_all(
        cls_from=Transaction,
        where_params=[Transaction.id == transaction_id, Transaction.user_id == user_id],
    )
    return DefaultResponseModel(status="success", detail="Transaction deleted")


@custom_core_decorator
async def delete_budget_implementation(budget_id: int, token: str):
    user_id = await get_current_user_id(token)
    await database_worker.custom_delete_all(
        cls_from=Budget,
        where_params=[Budget.id == budget_id, Budget.user_id == user_id],
    )
    return DefaultResponseModel(status="success", detail="Budget deleted")


@custom_core_decorator
async def delete_goal_implementation(goal_id: int, token: str):
    user_id = await get_current_user_id(token)
    await database_worker.custom_delete_all(
        cls_from=FinancialGoal,
        where_params=[FinancialGoal.id == goal_id, FinancialGoal.user_id == user_id],
    )
    return DefaultResponseModel(status="success", detail="Goal deleted")


@custom_core_decorator
async def delete_tag_implementation(tag_id: int, token: str):
    user_id = await get_current_user_id(token)
    await database_worker.custom_delete_all(
        cls_from=Tag, where_params=[Tag.id == tag_id, Tag.user_id == user_id]
    )
    return DefaultResponseModel(status="success", detail="Tag deleted")
