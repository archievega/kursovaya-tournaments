import uuid
from fastapi import Depends, Response
from fastapi.responses import JSONResponse
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    UUIDIDMixin,
    InvalidPasswordException,
    models
)
from typing import Generic

from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)

from fastapi_users.authentication.strategy import Strategy
from fastapi_users.types import DependencyCallable
from fastapi_users.db import SQLAlchemyUserDatabase
from pydantic import BaseModel

from src.auth.models import User
from src.auth.schemas import UserCreate, BearerResponseRefresh
from src.auth.utils import get_user_db


SECRET = "somesecret"


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def validate_password(
        self,
        password: str,
        user: UserCreate | User,
    ) -> None:
        if len(password) < 6:
            raise InvalidPasswordException(
                reason="Password should be at least 6 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Password should not contain e-mail"
            )


async def get_user_manager(
        user_db: SQLAlchemyUserDatabase = Depends(get_user_db)
):
    yield UserManager(user_db)


class BearerTransportRefresh(BearerTransport):
    async def get_login_response(self, token: str, refresh_token: str, user_id: uuid.UUID) -> Response:
        bearer_response = BearerResponseRefresh(
            access_token=token, 
            refresh_token=refresh_token,
            user_id=str(user_id), 
            token_type="bearer"
        )
        return JSONResponse(bearer_response.model_dump())

bearer_transport = BearerTransportRefresh(tokenUrl="api/v1/auth/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=300)

def get_refresh_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=259200)


class AuthenticationBackendRefresh(AuthenticationBackend):
    def __init__(
            self,
            *args,
            get_refresh_strategy: DependencyCallable[Strategy[models.UP, models.ID]],
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.get_refresh_strategy = get_refresh_strategy

    async def login(
            self,
            strategy: Strategy[models.UP, models.ID],
            user: models.UP,
    ) -> Response:
        token = await strategy.write_token(user)
        refresh_strategy = self.get_refresh_strategy()
        refresh_token = await refresh_strategy.write_token(user)
        return await self.transport.get_login_response(token=token, refresh_token=refresh_token, user_id=user.id)


auth_backend = AuthenticationBackendRefresh(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
    get_refresh_strategy=get_refresh_jwt_strategy
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True, verified=False)
