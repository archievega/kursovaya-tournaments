from uuid import UUID
from pydantic import BaseModel, UUID4

from fastapi_users import schemas


class PublicUser(BaseModel):
    id: UUID4
    username: str
    scores: int = 0
    class Config:
        from_attributes = True


class BearerResponseRefresh(BaseModel):
    access_token: str
    refresh_token: str
    user_id: str
    token_type: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class UserRead(schemas.BaseUser[UUID], PublicUser):
    pass


class UserCreate(schemas.BaseUserCreate):
    username: str


class UserUpdate(schemas.CreateUpdateDictModel):
    username: str
