import os
import uuid

from sanic.response import html, file
from sanic.exceptions import Forbidden

from . import bp
from src.videos.services.db_services import get_video_by_params

from src import get_template_loader


loader = get_template_loader()


# Only for debug
@bp.route('static/<path:path>')
async def static(request, path):
    if os.path.exists(os.path.join('static/', path)):
        return await file(f'static/{path}')
    else:
        raise Forbidden()


@bp.route('/')
async def home_view(request):
    template = loader.get_template('home.html')
    return html(await template.render_async())


@bp.route('video/')
async def video_view(request):
    video_uuid = request.get_args().get('video_uuid')
    if video_uuid:
        try:
            video_uuid = uuid.UUID(video_uuid)
        except ValueError:
            raise Forbidden()
        video = await get_video_by_params(uuid=video_uuid)
        template = loader.get_template('video.html')
        return html(await template.render_async(video=video))

