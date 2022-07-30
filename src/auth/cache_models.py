from typing import Dict
from uuid import UUID
from pydantic import BaseModel


class Session(BaseModel):
    username: str
    session_uuid: UUID
    user_uuid: UUID
    context: Dict
