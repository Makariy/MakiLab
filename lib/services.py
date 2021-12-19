from lib.models import User
from tortoise.exceptions import DoesNotExist


async def get_user_by_params(**params):
    """Returns user <src.feed.models.User> that suites the params,
    if user does not exist, returns None"""
    try:
        return await User.get(**params)
    except DoesNotExist:
        return None
