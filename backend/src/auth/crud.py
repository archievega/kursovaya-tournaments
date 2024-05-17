from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import Profile
from src.auth.schemas import CreateProfile
from sqlalchemy import insert


