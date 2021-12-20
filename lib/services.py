from uuid import uuid4
from lib.models import User
from tortoise.exceptions import DoesNotExist


async def get_user_by_params(**params):
    """Returns user <src.feed.models.User> that suites the params,
    if user does not exist, returns None"""
    try:
        return await User.get(**params)
    except DoesNotExist:
        return None


async def login_user(request, user: User):
    """Logins the user"""
    request.ctx.session['user_id'] = user.id
    request.ctx.session['csrf_token'] = uuid4().hex


async def logout_user(request):
    """Logs out the user"""
    request.ctx.session['user_id'] = None
    request.ctx.session['csrf_token'] = None

