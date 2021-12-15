import os
from jinja2 import Environment, FileSystemLoader


template_loader = Environment(
    loader=FileSystemLoader('src'),
    enable_async=True,
)

INSTALLED_APPS = [
    'src.feed',
]

DB_NAME = os.environ.get('DATABASE_NAME') or 'crypt'
DB_USER = os.environ.get('DATABASE_USER') or 'postgres'
DB_PASSWORD = os.environ.get('DATABASE_PASSWORD') or 'Kariy123'
DB_HOST = os.environ.get('DATABASE_HOST') or 'localhost'
DB_PORT = os.environ.get('DATABASE_PORT') or '5432'

