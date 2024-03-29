import uuid
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import TEXT, DATE, INTEGER,\
                                           ENUM as PgEnum, \
                                           TIMESTAMP as TS
from src.tournament.utils import PlayerStatus, TournamentStatus

from src.database import Base


class Match(Base):
    __tablename__ = "match"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    player1_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("profile.id")    
    )
    player2_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("profile.id")
    )
    winner: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("profile.id"),
        nullable=True
    )



class Tournament(Base):
    __tablename__ = "tournament"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    manager_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("profile.id"))
    title: Mapped[str] = mapped_column(
        TEXT()
    )
    description: Mapped[str] = mapped_column(TEXT(), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TS(), server_default=func.now()
    )
    starts_at: Mapped[datetime] = mapped_column(
        DATE()
    )
    max_players: Mapped[int] = mapped_column(INTEGER)
    address: Mapped[str] = mapped_column(TEXT())
    winner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("profile.id"), nullable=True)
    status: Mapped[TournamentStatus] = mapped_column(
        PgEnum(TournamentStatus)
    )



class Tournament_Player(Base):
    __tablename__ = "tournament_profile"
    tournament_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tournament.id"),
        primary_key=True
    )
    player_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("profile.id"),
        primary_key=True    
    )
    status: Mapped[PlayerStatus] = mapped_column(
        PgEnum(PlayerStatus, name="player_status")
    )
