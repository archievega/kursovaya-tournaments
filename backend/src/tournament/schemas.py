from pydantic import BaseModel, Field, UUID4
from datetime import datetime
from src.tournament.utils import TournamentStatus
from src.auth.schemas import PublicProfile

class TournamentBase(BaseModel):
    id: UUID4
    title: str
    starts_at: datetime
    address: str
    status: TournamentStatus

    class Config:
        from_attributes = True

class MatchBase(BaseModel):
    player_1: PublicProfile
    player_2: PublicProfile
    winner: PublicProfile | None = None


class Tournament(TournamentBase):
    matches: list[MatchBase]
    description: str
    members_count: int

class CreateTournament(BaseModel):
    title: str = Field(min_length=3, max_length=128)
    starts_at: datetime
    address: str
    max_players: int = Field(ge=2, default=2)

class CreateTournamentResponse(BaseModel):
    id: UUID4