from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import Profile
from src.auth.schemas import CreateProfile
from sqlalchemy import insert

async def get_profile(
        user_id: UUID,
        session: AsyncSession
) -> Profile | None:
    return await session.get(Profile, user_id)


async def create_profile(
        create_profile: CreateProfile,
        session: AsyncSession
) -> Profile:
    stmt = (
        insert(Profile)
        .values({Profile.id: create_profile.id,
                 Profile.username: create_profile.username,
                 Profile.role: create_profile.role})
        .returning(Profile)
    )
    profile: Profile = (await session.execute(stmt)).scalar_one()
    await session.flush()
    await session.commit()
    return profile

