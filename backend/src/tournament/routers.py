from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.database import get_async_session

from src.auth.utils import get_current_user
from src.auth.schemas import AuthUser, Role
from src.tournament import crud
from src.tournament.schemas import TournamentBase, \
                                   CreateTournament, \
                                   CreateTournamentResponse

router = APIRouter(
    prefix="/tournament",
    tags=["tournament"]
)

async def valid_manager(user: AuthUser = Depends(get_current_user)):
    if user.role == Role.MANAGER:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not a manager")

@router.get("/")
async def get_tournaments(user: AuthUser = Depends(get_current_user),
                          session: AsyncSession = Depends(get_async_session)
):
    tournaments = await crud.get_active_tournaments(session)
    tournament_schemas = [TournamentBase.model_validate(tournament) for tournament in tournaments]      
    return tournament_schemas


@router.post(
        "/create",
        status_code=status.HTTP_201_CREATED,
        response_model=CreateTournamentResponse)
async def create_tournament(
    tournament_data: CreateTournament,
    user: AuthUser = Depends(valid_manager),
    session: AsyncSession = Depends(get_async_session)
):
    tournament = await crud.create_tournament(user.id, tournament_data, session)
    return tournament