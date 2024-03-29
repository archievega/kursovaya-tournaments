from uuid import UUID
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from src.tournament.models import Tournament
from sqlalchemy import insert, select
from src.database import get_async_session
from src.tournament.utils import TournamentStatus
from src.tournament.schemas import CreateTournament


async def get_active_tournaments(
        session: AsyncSession = Depends(get_async_session)
) -> list[Tournament]:
    query = select(Tournament).where(Tournament.status == TournamentStatus.RUNNING)
    tournaments = await session.execute(query)
    return list(tournaments.scalars().all())


async def create_tournament(
        manager_id: UUID,
        tournament_data: CreateTournament,
        session: AsyncSession = Depends(get_async_session)
) -> Tournament:
    tournament = Tournament(manager_id=manager_id, **tournament_data.model_dump())
    session.add(tournament)
    await session.commit()
    await session.refresh(tournament)
    return tournament