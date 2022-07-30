import os


def start_new_app(app_name, config):
    """Creates the application with specified name <app_name>.
    Raises RuntimeError if the application with this name already exists"""
    app_dir = f'src/{app_name}'

    if os.path.exists(app_dir):
        raise RuntimeError(f'An application with name {app_name} already exists')

    os.mkdir(app_dir)
    models = open(os.path.join(app_dir, 'models.py'), 'w')
    tests = open(os.path.join(app_dir, 'tests.py'), 'w')

    app = open(os.path.join(app_dir, 'app.py'), 'w')
    app.write(f'\ndef get_blueprint():\n\tfrom .routes import bp\n\tbp.url_prefix = "{app_name}"\n\treturn bp\n')
    init = open(os.path.join(app_dir, '__init__.py'), 'w')
    init.write(f'from sanic import Blueprint\n\nbp = Blueprint(__package__)')
    routes = open(os.path.join(app_dir, 'routes.py'), 'w')
    routes.write('from . import bp\n\n# Create your routes here\n')

