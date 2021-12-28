import os
from sanic import Sanic


def _init_app(app, config):
    """Initializes the application"""
    app.ctx.config = config

    # Initialize sessions in the application
    from sanic_session import Session, InMemorySessionInterface
    Session(app, interface=InMemorySessionInterface())

    # Attach app events
    for event in config.app_events:
        for event_handler in config.app_events[event]:
            app.register_listener(event_handler, event)

    # Attach blueprints
    from .blueprint_routes import blue_print_routes
    for blueprint_getter in blue_print_routes:
        app.blueprint(blueprint_getter())


def create_app(config=None):
    """Creates and initializes the application"""
    _app = Sanic(os.environ.get('SANIC_APP_NAME') or 'sanic_application')
    _init_app(_app, config)
    return _app


def run_app(app, host='localhost', port=8000, workers=1):
    """Runs the application"""
    app.run(host=host, port=port, workers=workers)

