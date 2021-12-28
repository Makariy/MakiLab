from sanic import Sanic
from lib.database import init_database


def require_database(func):
    """Attaches the database to the application <app> so you can operate it inside the function"""
    async def _wrapper(app, *args, **kwargs):
        await init_database(app, None)
        return await func(app, *args, **kwargs)

    return _wrapper
