from datetime import datetime

from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import (
    TIMESTAMP as TS,
    TEXT,
    INTEGER
)
from sqlalchemy.schema import DefaultClause
from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTableUUID
)

from src.database import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"
    username: Mapped[str] = mapped_column(TEXT())
    scores: Mapped[int] = mapped_column(INTEGER(), server_default=DefaultClause("0"))
    created_at: Mapped[datetime] = mapped_column(TS(), server_default=func.now())
