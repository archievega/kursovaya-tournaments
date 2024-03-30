from pydantic import BaseModel, Field, UUID4
from datetime import datetime
from src.tournament.utils import TournamentStatus, \
                                 PlayerStatus
from src.auth.schemas import PublicProfile

class TournamentBase(BaseModel):
    id: UUID4
    title: str
    starts_at: datetime
    address: str
    status: TournamentStatus
    winner: PublicProfile | None = None

    class Config:
        from_attributes = True

class MatchBase(BaseModel):
    id: UUID4
    player_1: PublicProfile | None = None
    player_1_scores: int = Field(ge=0, default=0)
    player_2_scores: int = Field(ge=0, default=0)
    player_2: PublicProfile | None = None
    winner: PublicProfile | None = None

    class Config:
        from_attributes = True


class Tournament(TournamentBase):
    matches: list["MatchBase"] = []
    description: str | None = None
    players_count: int = len("")


class TournamentPlayers(TournamentBase):
    players: list["PublicProfile"] = []


class CreateTournament(BaseModel):
    title: str = Field(min_length=3, max_length=128)
    description: str = ""
    starts_at: datetime
    address: str
    max_players: int = Field(ge=2, default=2)


class CreateTournamentResponse(BaseModel):
    id: UUID4


class TournamentPlayer(BaseModel):
    player_id: UUID4
    tournament_id: UUID4
    status: PlayerStatus | str = "ACCEPTED"

    class Config:
        from_attributes = True


class SetMatchScore(BaseModel):
    player_1_scores: int = Field(ge=0, default=0)
    player_2_scores: int = Field(ge=0, default=0)