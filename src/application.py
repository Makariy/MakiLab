import os
from sanic import Sanic


def _init_app(app, config):
    """Initializes the application"""
    app.ctx.config = config

    for event in config.app_events:
        for event_handler in config.app_events[event]:
            app.register_listener(event_handler, event)

    from .blueprint_routes import blue_print_routes
    for blueprint_getter in blue_print_routes:
        app.blueprint(blueprint_getter())


def create_app(config):
    """Creates and initializes the sanic application"""
    app = Sanic(os.environ.get('SANIC_APP_NAME'))
    _init_app(app, config)
    return app


def run_app(app, host='localhost', port=8000, workers=1):
    """Runs the application"""
    app.run(host=host, port=port, workers=workers)
