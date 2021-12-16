import os
from sanic import Sanic
import tortoise


async def init_db_before_server_start(app: Sanic, loop):
    """Connect tortoise to the database. The function is being called before the server is started"""
    config = app.ctx.config
    await tortoise.Tortoise.init(
        db_url=f'postgres://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}',
        modules={
            'models': [f'{app}.models' for app in app.ctx.config.INSTALLED_APPS]
        }
    )
    await tortoise.Tortoise.generate_schemas()
