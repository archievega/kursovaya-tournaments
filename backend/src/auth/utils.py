from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase import Client
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.client import get_supabase_client
from src.auth.schemas import AuthUser
from uuid import UUID
from gotrue.types import UserResponse

from src.auth.crud import get_profile
from src.database import get_async_session

from src.auth.models import Profile



security = HTTPBearer()


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        supabase: Client = Depends(get_supabase_client),
        session: AsyncSession = Depends(get_async_session)
) -> AuthUser:
    try:
        supabase_user: UserResponse | None = supabase.auth.get_user(credentials.credentials)    
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid JWT token provided"
        )
    if supabase_user:
        db_profile: Profile | None = await get_profile(UUID(supabase_user.user.id), session)
        if db_profile:
            user = AuthUser(id=UUID(supabase_user.user.id), role=db_profile.role)
            return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid JWT token provided"
    )
