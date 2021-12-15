import os
from sanic import Sanic
from sanic import Blueprint
from sanic.response import json, html
from .models import *


app = Sanic.get_app(os.environ.get('SANIC_APP_NAME'))
loader = app.ctx.config.template_loader
bp = Blueprint(__package__)


@bp.route('/')
async def handle(request):
    template = loader.get_template('feed/templates/home.html')
    user = await User.create_user(username='Makar', password='Kariy123')
    return html(await template.render_async())

