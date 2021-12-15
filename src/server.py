import os
from sanic import Sanic


def _init_app(app, config):
    app.ctx.config = config

    from .app_events import app_events
    for event in app_events:
        for event_handler in app_events[event]:
            app.register_listener(event_handler, event)

    from .urls import blue_print_patterns
    for blueprint in blue_print_patterns:
        app.blueprint(blueprint)


def run_app(host='localhost', port=8000, workers=1, config=None):
    _app = Sanic(os.environ.get('SANIC_APP_NAME'))
    _init_app(_app, config)
    _app.run(host=host, port=port, workers=workers)
