from fastapi import HTTPException

from models.main_finance_account_model import Account
from models.main_finance_budget_model import Budget
from models.main_finance_category_model import Category
from models.main_finance_goal_model import FinancialGoal
from models.main_finance_transaction_model import M2M_TransactionTag, Tag, Transaction
from templates.base_models.finance_account import AccountModel
from templates.base_models.finance_budget import BudgetModel
from templates.base_models.finance_category import CategoryModel
from templates.base_models.finance_goal import GoalModel
from templates.base_models.finance_tag import TagModel
from templates.base_models.finance_transaction import TransactionModel
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
async def create_account_implementation(data, token: str):
    user_id = await get_current_user_id(token)
    instance = Account(user_id=user_id, **data.model_dump())
    result = await database_worker.custom_insert(
        cls_to=Account,
        data=[instance.as_dict()],
        returning=Account,
        return_unpacked=True,
    )
    return AccountModel(**result.as_dict())


@custom_core_decorator
async def create_category_implementation(data, token: str):
    user_id = await get_current_user_id(token)
    instance = Category(user_id=user_id, **data.model_dump())
    result = await database_worker.custom_insert(
        cls_to=Category,
        data=[instance.as_dict()],
        returning=Category,
        return_unpacked=True,
    )
    return CategoryModel(**result.as_dict())


@custom_core_decorator
async def create_transaction_implementation(data, token: str):
    user_id = await get_current_user_id(token)
    instance = Transaction(user_id=user_id, **data.model_dump(exclude_none=True))
    result = await database_worker.custom_insert(
        cls_to=Transaction,
        data=[instance.as_dict()],
        returning=Transaction,
        return_unpacked=True,
    )
    return TransactionModel(**result.as_dict())


@custom_core_decorator
async def create_budget_implementation(data, token: str):
    user_id = await get_current_user_id(token)
    instance = Budget(user_id=user_id, **data.model_dump())
    result = await database_worker.custom_insert(
        cls_to=Budget, data=[instance.as_dict()], returning=Budget, return_unpacked=True
    )
    return BudgetModel(**result.as_dict())


@custom_core_decorator
async def create_goal_implementation(data, token: str):
    user_id = await get_current_user_id(token)
    instance = FinancialGoal(user_id=user_id, **data.model_dump(exclude_none=True))
    result = await database_worker.custom_insert(
        cls_to=FinancialGoal,
        data=[instance.as_dict()],
        returning=FinancialGoal,
        return_unpacked=True,
    )
    return GoalModel(**result.as_dict())


@custom_core_decorator
async def create_tag_implementation(data, token: str):
    user_id = await get_current_user_id(token)
    instance = Tag(user_id=user_id, name=data.name)
    result = await database_worker.custom_insert(
        cls_to=Tag, data=[instance.as_dict()], returning=Tag, return_unpacked=True
    )
    return TagModel(**result.as_dict())


@custom_core_decorator
async def bind_tag_implementation(data, token: str):
    user_id = await get_current_user_id(token)
    transaction = await database_worker.custom_orm_select(
        cls_from=Transaction,
        where_params=[
            Transaction.id == data.transaction_id,
            Transaction.user_id == user_id,
        ],
        return_unpacked=True,
    )
    if not isinstance(transaction, Transaction):
        raise HTTPException(status_code=404, detail="Transaction not found")
    instance = M2M_TransactionTag(
        transaction_id=data.transaction_id,
        tag_id=data.tag_id,
        relevance_score=data.relevance_score,
    )
    await database_worker.custom_insert_do_nothing(
        cls_to=M2M_TransactionTag,
        index_elements=["transaction_id", "tag_id"],
        data=[instance.as_dict()],
    )
    return DefaultResponseModel(
        status="success", detail="Tag successfully bound to transaction"
    )
