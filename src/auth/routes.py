from . import bp

from sanic.request import Request
from sanic.response import json

from lib.exceptions import NotAuthorized

from utils.decorators import login_required
from .services.json_services import render_user
from .services.db_services import get_user_by_params, create_user
from .services.auth_services import login, logout

# Create your routes here


@bp.exception(NotAuthorized)
async def not_authorized(request: Request, exception: NotAuthorized):
    return json({
        "status": "fail",
        "error": exception.message
    }, status=exception.status_code)


@bp.route("login/", methods=["POST"])
async def login_view(request: Request):
    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
        return json({
            "status": "fail",
            "error": "Username or password not specified"
        })
    user = await get_user_by_params(username=username)
    if user is None:
        return json({
            "status": "fail",
            "error": "No such user with this username"
        })
    if not await user.compare_password(password):
        return json({
            "status": "fail",
            "error": "The password is not right"
        })
    response = json({
        "status": "success",
        **(await render_user(user))
    })
    await login(response, user)
    return response


@bp.route("signup/", methods=["POST"])
async def signup_view(request: Request):
    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
        return json({
            "status": "fail",
            "error": "Username or password not specified"
        })
    user, error = await create_user(username, password)
    if error is not None:
        return json({
            "status": "fail",
            "error": error
        })
    response = json({
        "status": "success",
        **(await render_user(user))
    })
    await login(response, user)
    return response


@bp.route("logout/", methods=["POST"])
@login_required
async def logout_view(request: Request):
    response = json({
        "status": "success",
    })
    await logout(response, request)
    return response


