from pydantic import BaseModel, Field, UUID4
from datetime import date

from src.tournament.models import Tournament as TournamentModel
from src.tournament.utils import TournamentStatus

from src.auth.schemas import PublicUser


class TournamentUser(BaseModel):
    player: PublicUser
    class Config:
        from_attributes = True


class TournamentBase(BaseModel):
    id: UUID4
    title: str
    starts_at: date
    address: str
    status: TournamentStatus
    winner: PublicUser | None = None

    class Config:
        from_attributes = True

class MatchBase(BaseModel):
    id: UUID4
    player_1: PublicUser | None = None
    player_1_scores: int = Field(ge=0, default=0)
    player_2_scores: int = Field(ge=0, default=0)
    player_2: PublicUser | None = None
    round: int
    winner: PublicUser | None = None

    class Config:
        from_attributes = True


class Tournament(TournamentBase):
    manager: PublicUser
    matches: list["MatchBase"]
    description: str | None = None
    players_count: int = 0
    players: list["PublicUser"]

    @classmethod
    def model_validate(
        cls: type[BaseModel],
        obj: TournamentModel
    ):
        players = [tournament_user.player for tournament_user in obj.players]
        return cls(
            id=obj.id,
            title=obj.title,
            starts_at=obj.starts_at,
            address=obj.address,
            status=obj.status,
            winner=obj.winner,
            manager=obj.manager,
            matches=obj.matches,
            description=obj.description,
            players_count=len(obj.players),
            players=players
        )


class CreateTournament(BaseModel):
    title: str = Field(min_length=3, max_length=128)
    description: str = ""
    starts_at: date
    address: str
    max_players: int = Field(ge=2, default=2)


class CreateTournamentResponse(BaseModel):
    id: UUID4



class SetMatchScore(BaseModel):
    player_1_scores: int = Field(ge=0, default=0)
    player_2_scores: int = Field(ge=0, default=0)