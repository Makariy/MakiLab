import os
from lib.database import init_database

from lib.cache.caches import DummyCache


INSTALLED_APPS = [
    'videos',
    'auth'
]

TESTING = False

app_events = {
    'main_process_start': [],
    'before_server_start': [],
    'after_server_start': [init_database],
}


SECRET_KEY = os.environ.get('SANIC_APP_SECRET_KEY') or 'd41ea53)122266ad84b503b70fd?4dbe167383375ceeb8ww8adsadwww29a2696d2c'
SESSION_EXPIRATION = 1 * 60 * 60

DB_NAME = os.environ.get('DATABASE_NAME') or 'makilab'
DB_USER = os.environ.get('DATABASE_USER') or 'postgres'
DB_PASSWORD = os.environ.get('DATABASE_PASSWORD') or 'postgres'
DB_HOST = os.environ.get('DATABASE_HOST') or 'localhost'
DB_PORT = os.environ.get('DATABASE_PORT') or '5432'

CACHE_CLASS = DummyCache
CACHE_HOST = os.environ.get('CACHE_HOST') or 'localhost'
CACHE_PORT = os.environ.get('CACHE_PORT') or 6379

MEDIA_LOADER_URL = os.environ.get('MEDIA_LOADER_URL') or 'http://192.168.1.144:9000'

CROWLING_URL = 'https://xvideos.com'
CROWLING_ROOT = 'https://xvideos.com'

DATA_SAVING_PATH = 'www/videos'
VIDEO_SAVING_PATH = f'{DATA_SAVING_PATH}/videos'
PREVIEW_SAVING_PATH = f'{DATA_SAVING_PATH}/previews'
