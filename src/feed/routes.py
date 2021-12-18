from src.feed import bp, loader
from sanic.response import json, html
from .services.db_services import *
from .json_services import *


@bp.route('/')
async def handle(request):
    template = loader.get_template('feed/templates/home.html')
    return html(await template.render_async())


@bp.route('get_last_posts/')
async def get_last_feed_posts_view(request):
    if request.method == 'GET':
        get_args = request.get_args()
        last_post_id = get_args.get('last_post_id')
        post_author_id = get_args.get('post_author_id')

        if post_author_id and post_author_id.isdigit():
            if last_post_id and last_post_id.isdigit():
                last_feed_posts = await get_last_feed_posts(post_author_id, start_post_id=last_post_id)
                return json(await render_feed_posts(last_feed_posts))
            else:
                last_feed_posts = await get_last_feed_posts(post_author_id)
                return json(await render_feed_posts(last_feed_posts))

    return json({'status': 'fail'})
