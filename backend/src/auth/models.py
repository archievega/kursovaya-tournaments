import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import TEXT, ENUM as PgEnum

from src.database import Base
from src.auth.schemas import Role

class Profile(Base):
    __tablename__ = "profile"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(
        TEXT(),
        unique=True,
        index=True,
        nullable=True,
    )
    icon_url: Mapped[str] = mapped_column(
        TEXT(),
        nullable=True    
    )
    info: Mapped[str] = mapped_column(
        TEXT(),
        nullable=True    
    )
    role: Mapped[Role] = mapped_column(
        PgEnum(Role, name="role")    
    )
