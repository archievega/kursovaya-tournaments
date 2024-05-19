import uuid
from fastapi import Depends, Response, status
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
from fastapi_users.openapi import OpenAPIResponseType

from src.auth.models import User
from src.auth.schemas import UserCreate, BearerResponseRefresh
from src.auth.utils import get_user_db

from src.config import settings

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.JWT_SECRET
    verification_token_secret = settings.JWT_SECRET

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
        return bearer_response
    
    @staticmethod
    def get_openapi_login_responses_success() -> OpenAPIResponseType:
        return {
            status.HTTP_200_OK: {
                "model": BearerResponseRefresh,
                "content": {
                    "application/json": {
                        "example": {
                            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1"
                            "c2VyX2lkIjoiOTIyMWZmYzktNjQwZi00MzcyLTg2Z"
                            "DMtY2U2NDJjYmE1NjAzIiwiYXVkIjoiZmFzdGFwaS"
                            "11c2VyczphdXRoIiwiZXhwIjoxNTcxNTA0MTkzfQ."
                            "M10bjOe45I5Ncu_uXvOmVV8QxnL-nZfcH96U90JaocI",
                            "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1"
                            "c2VyX2lkIjoiOTIyMWZmYzktNjQwZi00MzcyLTg2Z"
                            "DMtY2U2NDJjYmE1NjAzIiwiYXVkIjoiZmFzdGFwaS"
                            "11c2VyczphdXRoIiwiZXhwIjoxNTcxNTA0MTkzfQ."
                            "M10bjOe45I5Ncu_uXvOmVV8QxnL-nZfcH96U90JaocI",
                            "token_type": "bearer",
                        }
                    }
                },
            },
        }

bearer_transport = BearerTransportRefresh(tokenUrl="auth/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.JWT_SECRET, lifetime_seconds=300)

def get_refresh_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.JWT_SECRET, lifetime_seconds=259200)


class AuthenticationBackendRefresh(AuthenticationBackend):
    def __init__(
            self,
            name: str,
            transport: BearerTransportRefresh,
            get_strategy: DependencyCallable[Strategy[models.UP, models.ID]],
            get_refresh_strategy: DependencyCallable[Strategy[models.UP, models.ID]]
    ):
        self.name = name
        self.get_strategy = get_strategy
        self.get_refresh_strategy = get_refresh_strategy
        self.transport = transport

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
