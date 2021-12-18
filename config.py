import os
from jinja2 import Environment, FileSystemLoader
from src.app_events import init_db_before_server_start


template_loader = Environment(
    loader=FileSystemLoader('src'),
    enable_async=True,
)

INSTALLED_APPS = [
    'src.feed',
]

TESTING = False

app_events = {
    'before_server_start': [init_db_before_server_start],
    'after_server_start': [],
    'main_process_start': [],
}


DB_NAME = os.environ.get('DATABASE_NAME') or 'crypt'
DB_USER = os.environ.get('DATABASE_USER') or 'postgres'
DB_PASSWORD = os.environ.get('DATABASE_PASSWORD') or 'Kariy123'
DB_HOST = os.environ.get('DATABASE_HOST') or 'localhost'
DB_PORT = os.environ.get('DATABASE_PORT') or '5432'

MEDIA_LOADER_URL = os.environ.get('MEDIA_LOADER_URL') or 'http://192.168.1.144:9000'
