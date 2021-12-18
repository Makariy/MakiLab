import os
from sanic import Sanic
from sanic import Blueprint


application = Sanic.get_app(os.environ.get('SANIC_APP_NAME'))
loader = application.ctx.config.template_loader
bp = Blueprint(__package__)