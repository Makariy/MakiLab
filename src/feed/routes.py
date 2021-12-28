from sanic.response import json, html

from lib.services import get_user_by_params, login_user
from lib.decorators import login_required, redirect_if_logged, csrf_protect

from .services.db_services import *
from .json_services import *

from . import bp, get_template_loader


loader = get_template_loader()


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


# Just to test
@bp.post('login/')
@redirect_if_logged('/')
async def login(request):
    username = request.form.get('username')
    password = request.form.get('password')

    if username and password:
        user = await get_user_by_params(username=username)
        if user and await user.compare_password(password):
            await login_user(request, user)
            return json({'status': 'success'})

    return json({'status': 'fail'})


# Just to test
@bp.route('logout/', methods=['GET', 'POST'])
@csrf_protect
async def logout(request):
    if request.method == 'POST':
        code = request.form.get('code')
        return json({'status': 'success', 'code': code})

    else:
        csrf = request.ctx.csrf_token
        return html(f"""
            <form method='POST'>
                <input name='csrfmiddlewaretoken' value='{csrf}'/>
                <input name='code' type='text'/>
            </form>
        """)


# Just to test
@bp.get('info/')
@login_required
async def info(request):
    user_id = request.ctx.session.get('user_id')
    if user_id:
        user = await get_user_by_params(id=user_id)
        return json({
            'status': 'success',
            'user': {
                'username': user.username,
                'password': user.password,
                'uuid': str(user.uuid),
            }
        })

    return json({'status': 'fail'})
