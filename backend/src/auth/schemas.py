from pydantic import BaseModel, UUID4, AnyUrl
from pydantic.dataclasses import dataclass
from fastapi import Form
from enum import Enum

class Role(Enum):
    PLAYER: str = "PLAYER"
    MANAGER: str = "MANAGER"


class Token(BaseModel):
    access_token: str
    refresh_token: str


class AuthUser(BaseModel):
    id: UUID4
    role: Role
    class Config:
        from_attributes = True

class CreateProfile(BaseModel):
    id: UUID4
    username: str 
    role: Role


@dataclass
class RegistrateForm():
    username: str = Form()
    email: str = Form()
    password: str = Form()
    role: Role = Form()

class PublicProfile(BaseModel):
    icon_url: AnyUrl | None = None
    username: str 
    description: str
