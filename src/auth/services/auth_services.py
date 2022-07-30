from sanic.request import Request
from sanic.response import BaseHTTPResponse

from lib.models import User
from .cache_services import start_session, terminate_session

import config


async def login(response: BaseHTTPResponse, user: User):
    """
        Starts the session for user and sets the response session cookie
    """
    session = await start_session(user)
    response.cookies['session_uuid'] = str(session.session_uuid)
    response.cookies['session_uuid']['httponly'] = True
    response.cookies['session_uuid']['max-age'] = config.SESSION_EXPIRATION


async def logout(response: BaseHTTPResponse, request: Request):
    """
        Terminates the session and deletes the response session cookie
    """
    await terminate_session(request.ctx.session)
    del response.cookies['session_uuid']
