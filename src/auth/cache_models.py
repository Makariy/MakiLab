from uuid import UUID
from pydantic import BaseModel, Field


class Context(BaseModel):
    watched: list = Field(default_factory=list)


class Session(BaseModel):
    username: str
    session_uuid: UUID
    user_uuid: UUID
    context: Context = Field(default_factory=Context)

