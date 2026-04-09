import secrets

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from config import database_engine_async
from logs.log_worker import custom_core_decorator
from models.main_finance_user_model import User
from templates.base_models.finance_user import (
    DefaultResponseModel,
    FinanceChangePasswordRequest,
    RegisterRequestModel,
    ValidateBotTokenRequestModel,
)
from utils.internal_workers.auth_worker import AuthNamespace
from utils.internal_workers.database_worker import DatabaseWorkerAsync
from utils.internal_workers.redis_worker import redis_worker


database_worker = DatabaseWorkerAsync(database_engine_async)


@custom_core_decorator
async def register_implementation(data: RegisterRequestModel):
    exists = await database_worker.custom_orm_select(
        cls_from=User, where_params=[User.email == data.email]
    )
    if isinstance(exists, list) and exists:
        raise HTTPException(status_code=400, detail="Email already exists")

    user_instance = User(
        email=data.email,
        full_name=data.full_name,
        hashed_password=AuthNamespace._get_password_hash(data.password),
    )
    try:
        await database_worker.custom_insert(
            cls_to=User, data=[user_instance.as_dict()], returning=User
        )
    except IntegrityError as exception:
        raise HTTPException(status_code=400, detail=str(exception))
    return DefaultResponseModel(status="success", detail="User successfully created")


@custom_core_decorator
async def change_password_implementation(
    token: str, data: FinanceChangePasswordRequest
):
    user: User = await AuthNamespace.get_current_user(token=token)
    if not AuthNamespace._verify_password(data.current_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is invalid")
    await database_worker.custom_update(
        cls_to=User,
        where_params=[User.id == user.id],
        data={"hashed_password": AuthNamespace._get_password_hash(data.new_password)},
    )
    return DefaultResponseModel(
        status="success", detail="Password successfully changed"
    )


@custom_core_decorator
async def post_make_bot_token_implementation(token: str):
    user: User = await AuthNamespace.get_current_user(token=token)
    bot_token = secrets.token_urlsafe(48)
    await redis_worker.set(
        key=f"user_bot_token:{bot_token}",
        value={"id": user.id, "email": user.email},
        ex=60 * 10,
    )
    return DefaultResponseModel(status="success", detail=bot_token)


@custom_core_decorator
async def post_validate_bot_token_implementation(data: ValidateBotTokenRequestModel):
    user_info = await redis_worker.get(key=f"user_bot_token:{data.validation_token}")
    if not user_info:
        raise HTTPException(status_code=400, detail="Invalid validation token")
    await redis_worker.delete(f"user_bot_token:{data.validation_token}")
    return DefaultResponseModel(
        status="success",
        detail=f"Telegram account {data.telegram_id} validated for user {user_info['id']}",
    )
