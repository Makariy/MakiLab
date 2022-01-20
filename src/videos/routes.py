import os
import uuid

from . import bp
import config

from sanic.response import stream, json
from sanic.exceptions import Forbidden, MethodNotSupported

from .services.streaming_services import open_streaming_file
from .services.db_services import *
from src.videos.services.json_services import *

from sanic.response import StreamingHTTPResponse  # type


async def stream_video(request, video):
    video_path = os.path.join(config.VIDEO_SAVING_PATH, video.file_name)
    reader, status_code, content_length, content_range = \
        open_streaming_file(request, open(video_path, 'rb'))

    async def _stream_video(response: StreamingHTTPResponse):
        for chunk in reader:
            await response.write(chunk)

    headers = {
        'Accept-Ranges': 'bytes',
        'Content-Length': str(content_length),
        'Content-Range': content_range,
        'Cache-Control': 'no-cache'
    }
    return stream(_stream_video,
                  headers=headers,
                  status=status_code,
                  content_type='video/mp4')


@bp.route('stream/')
async def read_video_file(request, *args, **kwargs):
    video_uuid = request.get_args().get('video_uuid')
    if video_uuid:
        try:
            video_uuid = uuid.UUID(video_uuid)
        except ValueError:
            raise Forbidden()

        video = await get_video_by_params(uuid=video_uuid)
        if video:
            return await stream_video(request, video)

    raise Forbidden()


@bp.route('get_videos/')
async def get_videos(request):
    page = request.get_args().get('page') or '1'
    if page and page.isdigit():
        videos = await get_last_videos(20, int(page))
        rendered = await render_videos(videos)
        if len(videos) < 20:
            rendered['last'] = True
        else:
            rendered['last'] = False
        return json(rendered)

    raise Forbidden()

