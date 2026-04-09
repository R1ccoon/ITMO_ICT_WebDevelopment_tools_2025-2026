from config import database_engine_async
from fastapi import HTTPException
from models.main_finance_account_model import Account
from models.main_finance_budget_model import Budget
from models.main_finance_category_model import Category
from models.main_finance_goal_model import FinancialGoal
from models.main_finance_transaction_model import M2M_TransactionTag, Tag, Transaction
from models.main_finance_user_model import User
from templates.base_models.finance_account import AccountModel
from templates.base_models.finance_budget import BudgetModel
from templates.base_models.finance_category import CategoryModel
from templates.base_models.finance_goal import GoalModel
from templates.base_models.finance_transaction import (
    TransactionDetailsModel,
    TransactionTagModel,
)
from templates.base_models.finance_user import (
    FinanceUserDetailsResponse,
    FinanceUserListResponse,
    FinanceUserModel,
)
from logs.log_worker import custom_core_decorator
from utils.internal_workers.auth_worker import AuthNamespace
from utils.internal_workers.database_worker import DatabaseWorkerAsync

database_worker = DatabaseWorkerAsync(database_engine_async)


@custom_core_decorator
async def get_users_implementation(limit: int | None, offset: int | None, token: str):
    await AuthNamespace.get_current_user(token=token)
    users = await database_worker.custom_orm_select(
        cls_from=User, sql_limit=limit, offset=offset, order_by=[User.id.asc()]
    )
    total_count = await database_worker.count(cls_from=User)
    return FinanceUserListResponse(
        total_count=total_count[0],
        users=[FinanceUserModel(**u.as_dict()) for u in users],
    )


@custom_core_decorator
async def get_user_implementation(user_id: int, token: str):
    await AuthNamespace.get_current_user(token=token)
    user = await database_worker.custom_orm_select(
        cls_from=User, where_params=[User.id == user_id], return_unpacked=True
    )
    if not isinstance(user, User):
        raise HTTPException(status_code=404, detail="User not found")
    return FinanceUserModel(**user.as_dict())


@custom_core_decorator
async def get_user_details_implementation(user_id: int, token: str):
    await AuthNamespace.get_current_user(token=token)
    user = await database_worker.custom_orm_select(
        cls_from=User, where_params=[User.id == user_id], return_unpacked=True
    )
    if not isinstance(user, User):
        raise HTTPException(status_code=404, detail="User not found")

    accounts = await database_worker.custom_orm_select(
        cls_from=Account,
        where_params=[Account.user_id == user_id],
        order_by=[Account.id.asc()],
    )
    categories = await database_worker.custom_orm_select(
        cls_from=Category,
        where_params=[Category.user_id == user_id],
        order_by=[Category.id.asc()],
    )
    budgets = await database_worker.custom_orm_select(
        cls_from=Budget,
        where_params=[Budget.user_id == user_id],
        order_by=[Budget.id.asc()],
    )
    goals = await database_worker.custom_orm_select(
        cls_from=FinancialGoal,
        where_params=[FinancialGoal.user_id == user_id],
        order_by=[FinancialGoal.id.asc()],
    )
    transactions = await database_worker.custom_orm_select(
        cls_from=Transaction,
        where_params=[Transaction.user_id == user_id],
        order_by=[Transaction.id.asc()],
    )

    tx_ids = [transaction.id for transaction in transactions]
    tag_rows = []
    if tx_ids:
        tag_rows = await database_worker.custom_orm_select(
            cls_from=[
                M2M_TransactionTag.transaction_id,
                Tag.id,
                Tag.name,
                M2M_TransactionTag.relevance_score,
            ],
            select_from=[M2M_TransactionTag],
            join_on=[(Tag, Tag.id == M2M_TransactionTag.tag_id)],
            where_params=[M2M_TransactionTag.transaction_id.in_(tx_ids)],
        )

    tags_by_tx = {}
    for row in tag_rows:
        tags_by_tx.setdefault(row[0], []).append(
            TransactionTagModel(id=row[1], name=row[2], relevance_score=float(row[3]))
        )

    transaction_payload = []
    for transaction in transactions:
        transaction_payload.append(
            TransactionDetailsModel(
                **transaction.as_dict(), tags=tags_by_tx.get(transaction.id, [])
            )
        )

    return FinanceUserDetailsResponse(
        user=FinanceUserModel(**user.as_dict()),
        accounts=[AccountModel(**account.as_dict()) for account in accounts],
        categories=[CategoryModel(**category.as_dict()) for category in categories],
        budgets=[BudgetModel(**budget.as_dict()) for budget in budgets],
        goals=[GoalModel(**goal.as_dict()) for goal in goals],
        transactions=transaction_payload,
    )
