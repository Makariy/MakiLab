import os
from sanic import Sanic


def get_application() -> Sanic:
    """Returns the application"""
    return Sanic.get_app(os.environ.get('SANIC_APP_NAME'))


def get_config():
    """Returns the config"""
    return get_application().ctx.config


