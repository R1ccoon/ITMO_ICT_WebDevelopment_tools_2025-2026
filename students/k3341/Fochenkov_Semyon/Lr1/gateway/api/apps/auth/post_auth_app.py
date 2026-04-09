from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from utils.internal_workers.auth_worker import AuthNamespace
from templates.base_models.finance_user import (
    DefaultResponseModel,
    FinanceAuthTokenResponse,
    FinanceChangePasswordRequest,
    RegisterRequestModel,
    ValidateBotTokenRequestModel,
)
from templates.responses import TemplatesResponsesDataclass
from core.auth.post_auth_core import (
    change_password_implementation,
    post_make_bot_token_implementation,
    post_validate_bot_token_implementation,
    register_implementation,
)
from config import oauth2_scheme

post_auth_router = APIRouter()


@post_auth_router.post(
    "/login",
    responses={
        **TemplatesResponsesDataclass.template_404,
        **TemplatesResponsesDataclass.template_400,
        **TemplatesResponsesDataclass.template_500,
    },
    response_model=FinanceAuthTokenResponse,
    description="Эндпоинт логина"
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return await AuthNamespace.login(form_data=form_data)


@post_auth_router.post(
    "/register",
    responses={
        **TemplatesResponsesDataclass.template_404,
        **TemplatesResponsesDataclass.template_400,
        **TemplatesResponsesDataclass.template_500,
    },
    response_model=DefaultResponseModel,
    description="Эндпоинт для регистрации (mb legacy)"
)
async def register(data: RegisterRequestModel):
    return await register_implementation(data)


@post_auth_router.post(
    "/telegram/token/generate",
    responses={
        **TemplatesResponsesDataclass.template_404,
        **TemplatesResponsesDataclass.template_400,
        **TemplatesResponsesDataclass.template_500,
    },
    response_model=DefaultResponseModel,
    description="Эндпоинт для получения TTL токена"
)
async def post_make_bot_token(token: str = Depends(oauth2_scheme)):
    return await post_make_bot_token_implementation(token=token)


@post_auth_router.post(
    "/telegram/token/validate",
    responses={
        **TemplatesResponsesDataclass.template_404,
        **TemplatesResponsesDataclass.template_400,
        **TemplatesResponsesDataclass.template_500,
    },
    response_model=DefaultResponseModel,
    description="Эндпоинт для валидации токена"
)
async def post_validate_bot_token(data: ValidateBotTokenRequestModel):
    return await post_validate_bot_token_implementation(data=data)


@post_auth_router.post(
    "/change-password",
    responses={
        **TemplatesResponsesDataclass.template_404,
        **TemplatesResponsesDataclass.template_400,
        **TemplatesResponsesDataclass.template_500,
    },
    response_model=DefaultResponseModel,
    description="Смена пароля"
)
async def change_password(
    data: FinanceChangePasswordRequest,
    token: str = Depends(oauth2_scheme),
):
    return await change_password_implementation(token=token, data=data)
