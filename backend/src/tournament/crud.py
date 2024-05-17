from uuid import UUID
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from src.tournament.models import (
    Tournament,
    Match,
    Tournament_User
)
from src.tournament.schemas import CreateTournament, SetMatchScore
from src.tournament.utils import TournamentStatus

from src.auth.models import User



async def get_tournaments(
        session: AsyncSession
) -> list[Tournament]:
    query = (select(Tournament))
    tournaments = await session.execute(query)
    return list(tournaments.scalars().all())


async def create_tournament(
        user: User,
        tournament_data: CreateTournament,
        session: AsyncSession 
) -> Tournament:
    tournament = Tournament(manager_id=user.id, **tournament_data.model_dump())
    session.add(tournament)
    await session.commit()
    await session.refresh(tournament)
    return tournament


async def get_tournament(
        tournament_id: UUID,
        session: AsyncSession
) -> Tournament | None:
    tournament = await session.get(Tournament, tournament_id)
    return tournament


async def start_tournament(
        tournament: Tournament,
        session: AsyncSession
) -> Tournament:
    tournament.status = TournamentStatus.RUNNING
    await session.commit()
    return tournament


async def create_match(
        player_1_id: UUID,
        player_2_id: UUID | None,
        round: int,
        tournament: Tournament,
        session: AsyncSession
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
    

async def get_tournament_user(
        player: User,
        tournament: Tournament,
        session: AsyncSession
) -> Tournament_User | None:
     tour_player = await session.get(Tournament_User,
                                     (tournament.id,
                                      player.id))
     return tour_player


async def join_tournament(
        player: User,
        tournament: Tournament,
        session: AsyncSession
) -> Tournament:
        tour_player = Tournament_User(
            tournament_id=tournament.id,
            player_id=player.id
        )
        tournament.players.append(tour_player)
        session.add(tour_player)
        await session.commit()
        await session.refresh(tournament)
        return tournament
    


async def leave_tournament(
        player: User,
        tournament: Tournament,
        session: AsyncSession
):
    tour_player = await session.get(Tournament_User,
                                    (tournament.id,
                                     player.id))
    await session.delete(tour_player)
    await session.commit()
    return None


async def get_match(
        match_id: UUID,
        session: AsyncSession
) -> Match | None:
     match = await session.get(Match, match_id)
     return match


async def set_score(
          match_scores: SetMatchScore,
          match: Match,
          session: AsyncSession
) -> Match:
    match.player_1_scores = match_scores.player_1_scores
    match.player_2_scores = match_scores.player_2_scores
    if match_scores.player_1_scores > match_scores.player_2_scores:
        match.winner_id = match.player_1_id
    else:
        match.winner_id = match.player_2_id
    await session.commit()
    await session.refresh(match)
    return match


async def get_matches(
        tournament: Tournament,
        session: AsyncSession 
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
        session: AsyncSession
) -> list[Match]:
    stmt = (
        select(Match)
        .where(Match.tournament_id == tournament.id)
        .where(Match.round == round)
    )
    matches = await session.execute(stmt)
    return list(matches.scalars().all())


async def end_tournament(
        winner: User,
        tournament: Tournament,
        session: AsyncSession  
) -> Tournament:
    tournament.winner = winner
    winner.scores += 1
    tournament.status = TournamentStatus.ENDED
    await session.commit()
    return tournament


async def get_leaderboard(
        session: AsyncSession
) -> list[User]:
    stmt = (
        select(User)
        .order_by(User.scores.desc())
    )
    users = await session.execute(stmt)
    return list(users.scalars().all())
