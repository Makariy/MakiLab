from sanic.response import redirect
from lib.exceptions import ProhibitedException
from lib.services import get_user_by_params


def login_required(func):
    """Decorator which raises <lib.exceptions.ProhibitedException> if user is not logged"""
    async def _wrapper(request, *args, **kwargs):
        user_id = request.ctx.session.get('user_id')
        if user_id:
            user = await get_user_by_params(id=user_id)
            if user:
                request.ctx.user = user
                return await func(request, *args, **kwargs)
        raise ProhibitedException(message='Prohibited')

    return _wrapper


def redirect_if_logged(url='/'):
    """Returns a decorator that redirects if user is already logged in"""
    def _decorator(func):
        async def _wrapper(request, *args, **kwargs):
            user_id = request.ctx.session.get('user_id')
            if user_id:
                return redirect(url)
            return await func(request, *args, **kwargs)
        return _wrapper
    return _decorator


def csrf_protect(func):
    @login_required
    async def _wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            csrf_token = request.form.get('csrfmiddlewaretoken')
            if csrf_token and csrf_token == request.ctx.session['csrf_token']:
                return await func(request, *args, **kwargs)
            else:
                raise ProhibitedException(message='CSRF Token is not set or incorrect')
        else:
            request.ctx.csrf_token = request.ctx.session['csrf_token']
            return await func(request, *args, **kwargs)

    return _wrapper
