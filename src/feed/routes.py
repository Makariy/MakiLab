from sanic.response import json, html

from src.feed import bp, loader


@bp.route('/')
async def handle(request):
    template = loader.get_template('feed/templates/home.html')
    return html(await template.render_async())

