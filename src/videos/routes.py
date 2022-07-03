from . import bp

from sanic.response import json

from .services.db_services import *
from videos.services.json_services import *
from utils.converter import convert_string_to_uuid

from sanic.request import Request


@bp.route('get_videos/')
async def get_videos(request):
    page = request.get_args().get('page') or '1'
    if not page or not page.isdigit():
        return json({
            'status': "fail",
            'error': 'page not specified or is not a valid digit'
        })

    videos = await get_last_videos(20, int(page))
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

    return json({
        **rendered,
        'last': True if len(videos) < 20 else False,
        'status': 'success'
    })


@bp.route('video/')
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
    video = await get_video_by_params(uuid=video_uuid)
    return json({
        **(await render_video(video)),
        'status': 'success'
    })
