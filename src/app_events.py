import os
from sanic import Sanic
import tortoise


async def init_db_before_server_start(app: Sanic, loop):
    db_name = os.environ.get('DATABASE_NAME') or 'crypt'
    db_user = os.environ.get('DATABASE_USER') or 'postgres'
    db_password = os.environ.get('DATABASE_PASSWORD') or 'Kariy123'
    db_host = os.environ.get('DATABASE_HOST') or 'localhost'
    db_port = os.environ.get('DATABASE_PORT') or '5432'

    await tortoise.Tortoise.init(
        db_url=f'postgres://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',
        modules={
            'models': [f'{app}.models' for app in app.ctx.config.INSTALLED_APPS]
        }
    )
    await tortoise.Tortoise.generate_schemas()


app_events = {
    'before_server_start': [init_db_before_server_start]
}
