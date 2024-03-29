from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, status

from src.database import get_async_session

from src.auth.utils import get_current_user
from src.auth.models import Profile
from src.auth.schemas import AuthUser, Role
from src.tournament import crud
from src.tournament.schemas import TournamentBase, \
                                   CreateTournament, \
                                   CreateTournamentResponse, \
                                   Tournament as TournamentSchema, \
                                   TournamentPlayer as Tour_Player, \
                                   TournamentPlayers, SetMatchScore, \
                                   MatchBase 
from src.tournament.models import Tournament, Match
from src.tournament.utils import TournamentStatus
from uuid import UUID


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


async def valid_tournament(
        tournament_id: str,
        session: AsyncSession = Depends(get_async_session)
) -> Tournament:
    tournament = await crud.get_tournament(UUID(tournament_id), session)
    if not tournament:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tournament not found"
        )
    return tournament


async def valid_match(
        tournament_id: str,
        match_id: str,
        session: AsyncSession = Depends(get_async_session)
) -> Match:
    match = await crud.get_match(UUID(match_id), session)
    if match:
        if match.tournament_id == UUID(tournament_id):
            return match
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
            )


async def is_round_ended(
        round: int,
        tournament: Tournament = Depends(valid_tournament),
        session: AsyncSession = Depends(get_async_session)
) -> bool:
    matches = await crud.get_round_matches(
        round,
        tournament,
        session)
    ended = True
    for match in matches:
        if match.winner_id:
            pass
        else:
            ended = False
            break
    return ended


async def valid_tournament_owner(
        user: AuthUser = Depends(get_current_user),
        tournament: Tournament = Depends(valid_tournament)
) -> Tournament:
    if tournament.manager_id == user.id:
        return tournament
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You are not a manager of this tournament"
    )

async def get_round_winners(
    round: int,
    tournament: Tournament,
    session: AsyncSession = Depends(get_async_session)        
) -> list[Profile]:
    matches = await crud.get_round_matches(
        round,
        tournament,
        session)
    winners = []
    for match in matches:
        winners.append(match.winner)
    return winners


async def create_matches(
        players: list[Profile],
        round: int,
        tournament: Tournament,
        session: AsyncSession = Depends(get_async_session)
):
    players_count = len(players)
    for i in range(0, players_count-1, 2):
        await crud.create_match(
            players[i].id,
            players[i+1].id,
            round,
            tournament,
            session)
    if players_count % 2:
        await crud.create_match(
            players[-1].id,
            None,
            round,
            tournament,
            session
        ) 


@router.get("/")
async def get_tournaments(
    session: AsyncSession = Depends(get_async_session)
):
    tournaments = await crud.get_not_ended_tournaments(session)
    tournament_schemas = [TournamentBase.model_validate(tournament) for tournament in tournaments]      
    return tournament_schemas


@router.post(
        "/create",
        status_code=status.HTTP_201_CREATED,
        response_model=CreateTournamentResponse
)
async def create_tournament(
    tournament_data: CreateTournament,
    user: AuthUser = Depends(valid_manager),
    session: AsyncSession = Depends(get_async_session)
) -> Tournament:
    tournament = await crud.create_tournament(user.id, tournament_data, session)
    return tournament


async def end_tournament(
    winner_id: UUID,
    tournament: Tournament,
    session: AsyncSession = Depends(get_async_session)
):
    await crud.end_tournament(winner_id, tournament, session)
    


@router.get(
        "/{tournament_id}",
        response_model=TournamentSchema
)
async def get_tournament(
    tournament: Tournament = Depends(valid_tournament),
    session: AsyncSession = Depends(get_async_session)
):
    print(tournament.matches)
    tournament_schema = TournamentSchema.model_validate(tournament)
    return tournament_schema

@router.post(
    "/{tournament_id}/start"
)
async def start_tournament(
    tournament: Tournament = Depends(valid_tournament_owner),
    session: AsyncSession = Depends(get_async_session)
):
    if len(tournament.players) <= 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough players"    
    )
    await create_matches(tournament.players,
                         0,
                         tournament,
                         session)
    await crud.start_tournament(tournament, session)
    return {"status": "started"}


@router.post(
    "/{tournament_id}/join",
    response_model=Tour_Player
)
async def join_tournament(
    tournament: Tournament = Depends(valid_tournament),
    user: AuthUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    if tournament.status == TournamentStatus.WAITING:
        if await crud.get_tournament_player(user, tournament, session):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You already joined")
        tour_player = await crud.join_tournament(user, tournament, session)
        return Tour_Player.model_validate(tour_player)
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Wrong match condition")


@router.post(
    "/{tournament_id}/leave",
    status_code=status.HTTP_200_OK 
)
async def leave(
    tournament: Tournament = Depends(valid_tournament),
    user: AuthUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    if tournament.status == TournamentStatus.WAITING:
        if len(tournament.players) == tournament.max_players:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Max players count")
        if not (await crud.get_tournament_player(user, tournament, session)):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You are not in tournament")
        await crud.leave_tournament(user, tournament, session)
        return {"status": "Success"}
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Wrong match condition")
    

@router.post("/{tournament_id}/players")
async def get_tournament_players(
    tournament: Tournament = Depends(valid_tournament),
) -> TournamentPlayers:
    tournament_players = TournamentPlayers.model_validate(tournament)
    return tournament_players


@router.post(
        "/{tournament_id}/match/{match_id}",
        response_model=MatchBase)
async def set_score(
    match_score: SetMatchScore,
    match: Match = Depends(valid_match),
    tournament: Tournament = Depends(valid_tournament_owner),
    session: AsyncSession = Depends(get_async_session)
):
    match = await crud.set_score(
        match_score,
        match,
        session
    )
    if (await is_round_ended(match.round, tournament, session)):
        winners = await get_round_winners(match.round, tournament, session)
        if len(winners) == 1:
            await end_tournament(winners[0].id, tournament, session)
        await create_matches(winners, match.round+1, tournament, session)

    return MatchBase.model_validate(match)
    