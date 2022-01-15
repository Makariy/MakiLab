import os
import uuid

from sanic.response import html, file
from sanic.exceptions import Forbidden

from . import bp
import config
from src.videos.services.db_services import get_video_by_params
from src.videos.services.db_services import get_video_preview_by_params

from src import get_template_loader


loader = get_template_loader()


@bp.route('previews/<preview_uuid:str>')
async def preview(request, preview_uuid):
    try:
        preview_uuid = uuid.UUID(preview_uuid)
    except ValueError:
        raise Forbidden()
    preview = await get_video_preview_by_params(uuid=preview_uuid)
    if preview is None:
        raise Forbidden()
    else:
        path = os.path.join(config.PREVIEW_SAVING_PATH, preview.file_name)
        return await file(path)


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

