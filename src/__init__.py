import os
from sanic import Sanic
from jinja2 import Environment  # type


def get_application() -> Sanic:
    """Returns the application"""
    return Sanic.get_app(os.environ.get('SANIC_APP_NAME'))


def get_config():
    """Returns the config"""
    return get_application().ctx.config


def get_template_loader() -> Environment:
    """Returns the template loader"""
    return get_application().ctx.config.template_loader


