import os
from src import config


def start_new_app(app_name):
    """Creates the application with specified name <app_name>.
    Raises RuntimeError if the application with this name already exists"""
    app_dir = f'src/{app_name}'

    if os.path.exists(app_dir):
        raise RuntimeError(f'An application with name {app_name} already exists')

    os.mkdir(app_dir)
    models = open(os.path.join(app_dir, 'models.py'), 'w')
    tests = open(os.path.join(app_dir, 'tests.py'), 'w')
    app = open(os.path.join(app_dir, 'app.py'), 'w')
    app.write(f'def get_blueprint():\n    raise NotImplemented("src.{app_name}.app.get_blueprint is not implemented")')


