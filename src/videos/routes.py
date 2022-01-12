import uuid

from . import bp

from sanic.response import stream, json
from sanic.exceptions import Forbidden

from .services.streaming_services import open_streaming_file
from .services.db_services import *
from src.videos.services.json_services import *


async def stream_video(request, video):
    reader, status_code, content_length, content_range = \
        open_streaming_file(request, open('data/' + video.file_name, 'rb'))

    async def _stream_video(response):
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
    videos = await get_last_videos(20)
    return json(await render_videos(videos))


