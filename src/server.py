from sanic import Sanic
from .urls import blue_print_patterns
from .app_events import app_events

_app = Sanic(__name__)


def _init_app(app, config):
    app.ctx.config = config

    for event in app_events:
        for event_handler in app_events[event]:
            app.register_listener(event_handler, event)

    for pattern in blue_print_patterns:
        app.blueprint(pattern[0], url_prefix=pattern[1])


from sanic.response import json
from .feed.models import *


@_app.route('/')
async def handle(request):
    user = await User.create_user(username='Makar', password='Kariy123')
    return json({'status': 'Zaebis', 'username': user.username})


def run_app(host='localhost', port=8000, workers=1, config=None):
    _init_app(_app, config)
    _app.run(host=host, port=port, workers=workers)
