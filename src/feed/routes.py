from src.feed import bp, loader
from sanic.response import json, html
from .services.db_services import *
from .json_services import *
from lib.sessions import SessionCreator


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


# Only on custom session mechanism test
@bp.route('login/')
async def login(request):
    get_args = request.get_args()
    username = get_args.get('username')
    password = get_args.get('password')
    if username and password:
        user = await User.get(username=username)
        if await user.compare_password(password):
            return json({
                'status': 'success',
                'token': await SessionCreator.create_session(user)
            })
    return json({'status': 'fail'})


# Only on custom sessions mechanism test
@bp.route('info/')
async def info(request):
    get_args = request.get_args()
    token = get_args.get('token')
    if token:
        user = await SessionCreator.get_user_by_token(token)
        return json({
            'status': 'success',
            'user': {
                'username': user.username,
                'password': user.password,
                'uuid': str(user.uuid),
                'id': user.id,
            }
        })
    return json({'status': 'fail'})

