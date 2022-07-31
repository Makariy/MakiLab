from . import bp

from sanic.response import json

from .services.db_services import *
from .services.cache_services import increment_views, add_is_videos_watched
from videos.services.json_services import *
from utils.converter import convert_string_to_uuid
from utils.decorators import attach_session

from sanic.request import Request


@bp.route('get_videos/')
@attach_session
async def get_videos_view(request):
    page = request.get_args().get('page') or '1'
    if not page or not page.isdigit():
        return json({
            'status': "fail",
            'error': 'page not specified or is not a valid digit'
        })

    videos = await get_videos(prefetch_author=True, count=20, page=int(page))
    if not videos:
        return json({
            'status': 'fail',
            'error': 'could not get videos'
        })

    rendered = await render_videos(videos)
    if not rendered:
        return json({
            'status': 'fail',
            'error': 'could not render the videos'
        })

    if request.ctx.user and request.ctx.session:
        rendered = await add_is_videos_watched(rendered, request.ctx.user, request.ctx.session)
    return json({
        **rendered,
        'last': True if len(videos) < 20 else False,
        'status': 'success'
    })


@bp.route('video/')
@attach_session
async def video_view(request: Request):
    video_uuid = request.get_args().get('video_uuid')
    if not video_uuid:
        return json({
            'status': 'fail',
            'error': 'video_uuid is not specified'
        })
    video_uuid = convert_string_to_uuid(video_uuid)
    if not video_uuid:
        return json({
            'status': 'fail',
            'error': 'video_uuid is not a valid uuid'
        })
    video = await get_video_by_params(prefetch_author=True, uuid=video_uuid)
    if request.ctx.user and request.ctx.session:
        await increment_views(video, request.ctx.user, request.ctx.session)

    if video is None:
        return json({
            'status': 'fail',
            'error': 'video with this video_uuid does not exists'
        })
    return json({
        **(await render_video(video)),
        'status': 'success'
    })
