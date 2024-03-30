from uuid import UUID
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from src.tournament.models import Tournament, Match, \
                                  Tournament_Player
from sqlalchemy import select
from src.database import get_async_session
from src.tournament.utils import TournamentStatus
from src.tournament.schemas import CreateTournament, SetMatchScore
from src.auth.schemas import AuthUser
from src.auth.crud import get_profile


async def  get_tournaments(
        session: AsyncSession = Depends(get_async_session)
) -> list[Tournament]:
    query = (select(Tournament))
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


async def get_tournament(
        tournament_id: UUID,
        session: AsyncSession = Depends(get_async_session)
) -> Tournament | None:
    tournament = await session.get(Tournament, tournament_id)
    return tournament


async def start_tournament(
        tournament: Tournament,
        session: AsyncSession = Depends(get_async_session)
) -> Tournament:
    tournament.status = TournamentStatus.RUNNING
    await session.commit()
    return tournament


async def create_init_matches(
        tournament: Tournament,
        session: AsyncSession = Depends(get_async_session)
):
    players = tournament.players


async def create_match(
        player_1_id: UUID,
        player_2_id: UUID | None,
        round: int,
        tournament: Tournament,
        session: AsyncSession = Depends(get_async_session)
):
    if not player_2_id:
        match = Match(
            tournament_id=tournament.id,
            player_1_id=player_1_id,
            player_2_id=player_2_id,
            round=round,
            player_1_scores=1,
            winner_id=player_1_id)
    else:
        match = Match(
                tournament_id=tournament.id,
                player_1_id=player_1_id,
                round=round,
                player_2_id=player_2_id)
    session.add(match)
    await session.commit()
    await session.refresh(match)
    return match
    

async def get_tournament_player(
        player: AuthUser,
        tournament: Tournament,
        session: AsyncSession = Depends(get_async_session)
) -> Tournament_Player | None:
     tour_player = await session.get(Tournament_Player,
                                     (tournament.id,
                                      player.id))
     print(tour_player)
     return tour_player


async def join_tournament(
        player: AuthUser,
        tournament: Tournament,
        session: AsyncSession = Depends(get_async_session)
) -> Tournament_Player:
        tour_player = Tournament_Player(
             tournament_id=tournament.id,
             player_id=player.id
        )
        session.add(tour_player)
        await session.commit()
        await session.refresh(tour_player)
        return tour_player
    


async def leave_tournament(
        player: AuthUser,
        tournament: Tournament,
        session: AsyncSession = Depends(get_async_session)
):
    tour_player = await session.get(Tournament_Player,
                                    (tournament.id,
                                     player.id))
    await session.delete(tour_player)
    await session.commit()
    return None


async def get_match(
        match_id: UUID,
        session: AsyncSession = Depends(get_async_session)
) -> Match | None:
     match = await session.get(Match, match_id)
     return match


async def set_score(
          match_scores: SetMatchScore,
          match: Match,
          session: AsyncSession = Depends(get_async_session)) -> Match:
    match.player_1_scores = match_scores.player_1_scores
    match.player_2_scores = match_scores.player_2_scores
    if match_scores.player_1_scores > match_scores.player_2_scores:
        match.winner_id = match.player_1_id
    else:
        match.winner_id = match.player_1_id
    await session.commit()
    await session.refresh(match)
    return match


async def get_matches(
        tournament: Tournament,
        session: AsyncSession = Depends(get_async_session)
) -> list[Match]:
    stmt = (
        select(Match)
        .where(Match.tournament_id == tournament.id)
        )
    matches = await session.execute(stmt)
    return list(matches.scalars().all())


async def get_round_matches(
        round: int,
        tournament: Tournament,
        session: AsyncSession = Depends(get_async_session)
) -> list[Match]:
    stmt = (
        select(Match)
        .where(Match.tournament_id == tournament.id)
        .where(Match.round == round)
        )
    matches = await session.execute(stmt)
    return list(matches.scalars().all())


async def end_tournament(
        winner_id: UUID,
        tournament: Tournament,
        session: AsyncSession = Depends(get_async_session)        
) -> Tournament:
    tournament.winner_id = winner_id
    player = await get_profile(winner_id, session)
    if player:
        player.scores += 1
    tournament.status = TournamentStatus.ENDED
    await session.commit()
    return tournament
