from typing import Tuple, Optional
from sanic import Request
from lib.exceptions import NotAuthorized

from auth.cache_models import Session
from auth.models import User
from auth.services.db_services import get_user_by_params
from auth.services.cache_services import get_session_by_uuid


async def get_session_and_user(request: Request) -> Tuple[Optional[Session], Optional[User]]:
    try:
        session_uuid = request.cookies.get("session_uuid")
        if not session_uuid:
            raise NotAuthorized()

        session = await get_session_by_uuid(session_uuid)
        if session is None:
            raise NotAuthorized()

        user = await get_user_by_params(uuid=session.user_uuid)
        if user is None:
            raise NotAuthorized()

        return session, user
    except NotAuthorized:
        return None, None


def attach_session(view):
    async def wrapper(request: Request, *args, **kwargs):
        session, user = await get_session_and_user(request)
        request.ctx.user = user
        request.ctx.session = session
        return await view(request, *args, **kwargs)
    return wrapper


def login_required(view):
    async def wrapper(request: Request, *args, **kwargs):
        session, user = await get_session_and_user(request)
        if session is None or user is None:
            raise NotAuthorized()

        request.ctx.user = user
        request.ctx.session = session
        return await view(request, *args, **kwargs)

    return wrapper
