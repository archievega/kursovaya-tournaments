from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, Response, status

from fastapi.security import OAuth2PasswordRequestForm
from src.database import get_async_session

from gotrue.types import AuthResponse
from supabase.client import Client
from src.auth.client import get_supabase_client
from src.auth.schemas import Token, RegistrateForm, CreateProfile
from src.auth.crud import create_profile
from uuid import UUID



router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post(
        "/login",
        status_code=status.HTTP_200_OK,
        response_model = Token
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    supabase: Client = Depends(get_supabase_client)
):
    try:
        supabase_session: AuthResponse = supabase.auth.sign_in_with_password(
            {"email": form_data.username,
             "password": form_data.password}
        )
        if supabase_session.session:
            return Token(
                access_token=supabase_session.session.access_token,
                refresh_token=supabase_session.session.refresh_token
            )
    except Exception as e:
        print(e)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Wrong credentials")


@router.post(
        "/register",
        status_code=status.HTTP_201_CREATED)
async def register(
    form_data: RegistrateForm,
    supabase: Client = Depends(get_supabase_client),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        supabase_session: AuthResponse = supabase.auth.sign_up(
            {"email": form_data.email,
            "password": form_data.password}
        )
        if supabase_session.session:
            user_id = UUID(supabase_session.user.id)
            user_data = CreateProfile(
                id=user_id,
                username=form_data.username,
                role=form_data.role)
            await create_profile(user_data, session)
            return {
                "access_token":supabase_session.session.access_token,
                "refresh_token":supabase_session.session.refresh_token
            }
    except Exception as e:
        print(e)
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "Wrong credentials")