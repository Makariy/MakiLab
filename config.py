import os
from jinja2 import Environment, FileSystemLoader


template_loader = Environment(
    loader=FileSystemLoader('src'),
    enable_async=True,
)

INSTALLED_APPS = [
    'src.feed',
]


