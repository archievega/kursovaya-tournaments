from fastapi import (
    APIRouter,
    Depends,
    Response,
    HTTPException,
    status
)

from src.auth.client import (
    auth_backend,
    fastapi_users,
    get_jwt_strategy,
    get_refresh_jwt_strategy,
    UserManager,
    get_user_manager
)

from fastapi_users.authentication import JWTStrategy

from src.auth.schemas import (
    UserCreate,
    UserRead,
    UserUpdate,
    PublicUser,
    RefreshTokenSchema
)


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/token")
async def refresh_jwt(
    refresh_token: RefreshTokenSchema,
    jwt_strategy: JWTStrategy = Depends(get_jwt_strategy),
    refresh_jwt_strategy: JWTStrategy = Depends(get_refresh_jwt_strategy),
    mgr: UserManager = Depends(get_user_manager)
):
    user = await refresh_jwt_strategy.read_token(refresh_token.refresh_token, mgr)
    if user:
        return await auth_backend.login(jwt_strategy, user)


router.include_router(
    fastapi_users.get_auth_router(auth_backend)
)


router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)
