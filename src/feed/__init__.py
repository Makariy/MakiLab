import os
from sanic import Sanic
from sanic import Blueprint


def get_application():
    return Sanic.get_app(os.environ.get('SANIC_APP_NAME'))


def get_template_loader():
    return get_application().ctx.config.template_loader


bp = Blueprint(__package__.replace('.', '_'))
