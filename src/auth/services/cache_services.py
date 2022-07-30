import json
from uuid import uuid4
from pydantic import ValidationError
from typing import Union, Dict

from auth.models import User
from auth.cache_models import Session
from lib.cache.cache import Cache


async def get_session_by_uuid(session_uuid: str) -> Union[Session, None]:
    raw_session = await Cache.get(session_uuid)
    if raw_session is None:
        return None
    try:
        session = json.loads(raw_session)
        return Session.validate(session)

    except ValidationError:
        return None


async def start_session(user: User) -> Session:
    session = Session.construct(
        username=user.username,
        user_uuid=user.uuid,
        session_uuid=uuid4(),
        context={}
    )
    await Cache.set(str(session.session_uuid), session.json())
    return session


async def terminate_session(session: Session):
    await Cache.delete(str(session.session_uuid))

