import os
import importlib
from sanic import Sanic


def _register_events(app, config):
    for event in config.app_events:
        for event_handler in config.app_events[event]:
            app.register_listener(event_handler, event)


def _register_blueprints(app, config):
    for app_name in config.INSTALLED_APPS:
        try:
            module = importlib.import_module(app_name + ".app")
            app.blueprint(module.get_blueprint())
        except ImportError as e:
            print(f"Cannot import {app_name}.app module")
            raise e
        except AttributeError as e:
            print(f"Cannot import get_blueprint from {app_name}.app module")
            raise e


def _init_app(app, config):
    app.ctx.config = config
    _register_events(app, config)
    _register_blueprints(app, config)


def create_app(config):
    """Creates and initializes the sanic application"""
    app = Sanic(os.environ.get('SANIC_APP_NAME'))
    _init_app(app, config)
    return app


def run_app(app, host='localhost', port=8000, workers=1):
    """Runs the application"""
    app.run(host=host, port=port, workers=workers)
