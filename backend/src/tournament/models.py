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
from src.auth.models import Profile


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
        PgEnum(PlayerStatus, name="player_status"),
        default=PlayerStatus.ACCEPTED
    )


class Match(Base):
    __tablename__ = "match"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    tournament_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tournament.id")
    )
    round: Mapped[int] = mapped_column(
        INTEGER()
    )
    tournament: Mapped["Tournament"] = relationship(back_populates="matches")
    player_1_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("profile.id"),
        nullable=True
    )
    player_1: Mapped["Profile"] = relationship(lazy="selectin", foreign_keys=[player_1_id])
    player_1_scores: Mapped[int] = mapped_column(INTEGER(), nullable=True)
    player_2_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("profile.id"),
        nullable=True
    )
    player_2: Mapped[Profile] = relationship(lazy="selectin", foreign_keys=[player_2_id])
    player_2_scores: Mapped[int] = mapped_column(INTEGER(), nullable=True)

    winner_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("profile.id"),
        nullable=True
    )
    winner: Mapped[Profile] = relationship(lazy="selectin", foreign_keys=[winner_id])


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
    players: Mapped[list[Profile]] = relationship(secondary=Tournament_Player.__table__, lazy="selectin")
    max_players: Mapped[int] = mapped_column(INTEGER())
    matches: Mapped[list[Match]] = relationship(back_populates="tournament", lazy="selectin")
    address: Mapped[str] = mapped_column(TEXT())
    winner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("profile.id"), nullable=True)
    status: Mapped[TournamentStatus] = mapped_column(
        PgEnum(TournamentStatus, name="tournament_status"),
        default=TournamentStatus.WAITING
    )

    def __repr__(self):
        return f"{self.id, self.title}"