import logging
from datetime import datetime, timedelta

from config import admin_settings, database_engine_async
from models.main_finance_account_model import Account
from models.main_finance_budget_model import Budget
from models.main_finance_category_model import Category
from models.main_finance_goal_model import FinancialGoal
from models.main_finance_transaction_model import M2M_TransactionTag, Tag, Transaction
from models.main_finance_user_model import User
from utils.internal_workers.auth_worker import AuthNamespace
from utils.internal_workers.database_worker import DatabaseWorkerAsync

database_worker = DatabaseWorkerAsync(database_engine_async)
logger = logging.getLogger("app.schedulers.data_init")


async def init_default_user():
    hashed_password = AuthNamespace._get_password_hash(admin_settings.ADMIN_PASSWORD)
    user = await database_worker.custom_upsert(
        cls_to=User,
        index_elements=["email"],
        data=[
            User(
                email="admin@example.com",
                full_name="string",
                hashed_password=hashed_password,
            ).as_dict()
        ],
        update_set=["full_name", "hashed_password", "is_active"],
        returning=User,
        return_unpacked=True,
    )
    return user


async def init_default_categories(user_id: int):
    categories = [
        {"name": "Salary", "direction": "income", "is_system": True},
        {"name": "Freelance", "direction": "income", "is_system": True},
        {"name": "Food", "direction": "expense", "is_system": True},
        {"name": "Transport", "direction": "expense", "is_system": True},
        {"name": "Utilities", "direction": "expense", "is_system": True},
    ]
    for item in categories:
        await database_worker.custom_upsert(
            cls_to=Category,
            index_elements=["user_id", "name", "direction"],
            data=[Category(user_id=user_id, **item).as_dict()],
            update_set=["is_system"],
        )


async def init_default_account(user_id: int) -> Account:
    account = await database_worker.custom_upsert(
        cls_to=Account,
        index_elements=["user_id", "name"],
        data=[
            Account(
                user_id=user_id,
                name="Main Card",
                currency_code="RUB",
                balance=100000.0,
                is_archived=False,
            ).as_dict()
        ],
        update_set=["currency_code", "balance", "is_archived"],
        returning=Account,
        return_unpacked=True,
    )
    return account


async def init_default_budget(user_id: int):
    expense_category = await database_worker.custom_orm_select(
        cls_from=Category,
        where_params=[Category.user_id == user_id, Category.name == "Food"],
        return_unpacked=True,
    )
    if not expense_category:
        return
    await database_worker.custom_upsert(
        cls_to=Budget,
        index_elements=["user_id", "category_id", "period"],
        data=[
            Budget(
                user_id=user_id,
                category_id=expense_category.id,
                period="monthly",
                limit_amount=30000.0,
                spent_amount=0.0,
            ).as_dict()
        ],
        update_set=["limit_amount", "spent_amount"],
    )


async def init_default_goal(user_id: int):
    await database_worker.custom_upsert(
        cls_to=FinancialGoal,
        index_elements=["user_id", "name"],
        data=[
            FinancialGoal(
                user_id=user_id,
                name="Emergency Fund",
                target_amount=500000.0,
                current_amount=50000.0,
                deadline=datetime.utcnow() + timedelta(days=365),
                status="active",
            ).as_dict()
        ],
        update_set=["target_amount", "current_amount", "deadline", "status"],
    )


async def init_default_tags(user_id: int):
    for tag_name in ["important", "recurring", "planned"]:
        await database_worker.custom_upsert(
            cls_to=Tag,
            index_elements=["user_id", "name"],
            data=[Tag(user_id=user_id, name=tag_name).as_dict()],
            update_set=["name"],
        )


async def init_default_transaction(user_id: int, account_id: int):
    category = await database_worker.custom_orm_select(
        cls_from=Category,
        where_params=[Category.user_id == user_id, Category.name == "Salary"],
        return_unpacked=True,
    )
    if not category:
        return

    rows = await database_worker.custom_orm_select(
        cls_from=Transaction,
        where_params=[
            Transaction.user_id == user_id,
            Transaction.account_id == account_id,
            Transaction.category_id == category.id,
            Transaction.amount == 100000.0,
            Transaction.transaction_type == "income",
        ],
        order_by=[Transaction.id.asc()],
        sql_limit=1,
    )
    transaction = rows[0] if rows else None
    if not transaction:
        inserted = await database_worker.custom_insert(
            cls_to=Transaction,
            data=[
                Transaction(
                    user_id=user_id,
                    account_id=account_id,
                    category_id=category.id,
                    transaction_type="income",
                    amount=100000.0,
                    note="Initial salary transaction",
                ).as_dict()
            ],
            returning=Transaction,
        )
        transaction = inserted[0] if isinstance(inserted, list) and inserted else None

    default_tag = await database_worker.custom_orm_select(
        cls_from=Tag,
        where_params=[Tag.user_id == user_id, Tag.name == "important"],
        return_unpacked=True,
    )
    if transaction and default_tag:
        await database_worker.custom_insert_do_nothing(
            cls_to=M2M_TransactionTag,
            index_elements=["transaction_id", "tag_id"],
            data=[
                M2M_TransactionTag(
                    transaction_id=transaction.id,
                    tag_id=default_tag.id,
                    relevance_score=1.0,
                ).as_dict()
            ],
        )


async def must_init(app=None):
    try:
        user = await init_default_user()
        await init_default_categories(user.id)
        account = await init_default_account(user.id)
        await init_default_budget(user.id)
        await init_default_goal(user.id)
        await init_default_tags(user.id)
        await init_default_transaction(user.id, account.id)
        logger.info("Default finance data initialized")
    except Exception as exception:
        logger.error(f"Failed to initialize default finance data: {exception}")
