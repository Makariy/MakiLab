import importlib
import os
from sanic import Sanic
import tortoise


async def init_db_before_server_start(app: Sanic, loop):
    """Connect tortoise to the database. The function is being called before the server is started"""
    config = app.ctx.config
    models_packages = ['lib.models']
    for app in app.ctx.config.INSTALLED_APPS:
        try:
            importlib.import_module(f'{app}.models')
        except ImportError:
            continue
        models_packages.append(f'{app}.models')

    await tortoise.Tortoise.init(
        db_url=f'postgres://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}',
        modules={
            'models': models_packages,
        }
    )
    await tortoise.Tortoise.generate_schemas()
