import os
from jinja2 import Environment, FileSystemLoader
from lib.database import init_database


template_loader = Environment(
    loader=FileSystemLoader('templates'),
    enable_async=True,
)

INSTALLED_APPS = [
    'videos',
]

TESTING = False

app_events = {
    'main_process_start': [],
    'before_server_start': [],
    'after_server_start': [init_database],
}


SECRET_KEY = os.environ.get('SANIC_APP_SECRET_KEY') or 'd41ea53)122266ad84b503b70fd?4dbe167383375ceeb8ww8adsadwww29a2696d2c'

DB_NAME = os.environ.get('DATABASE_NAME') or 'makilab'
DB_USER = os.environ.get('DATABASE_USER') or 'postgres'
DB_PASSWORD = os.environ.get('DATABASE_PASSWORD') or 'postgres'
DB_HOST = os.environ.get('DATABASE_HOST') or 'localhost'
DB_PORT = os.environ.get('DATABASE_PORT') or '5432'

MEDIA_LOADER_URL = os.environ.get('MEDIA_LOADER_URL') or 'http://192.168.1.144:9000'

CROWLING_URL = 'https://xvideos.com'
CROWLING_ROOT = 'https://xvideos.com'

DATA_SAVING_PATH = 'www/videos'
VIDEO_SAVING_PATH = f'{DATA_SAVING_PATH}/videos'
PREVIEW_SAVING_PATH = f'{DATA_SAVING_PATH}/previews'
