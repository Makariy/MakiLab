from tortoise.exceptions import DoesNotExist

from lib.models import User
from src.videos.models import Video, VideoPreview


async def get_video_by_params(**params):
    try:
        return await Video.get(**params)
    except DoesNotExist:
        return None


async def get_video_preview_by_params(**params):
    try:
        return await VideoPreview.get(**params)
    except DoesNotExist:
        return None


async def get_last_videos(count=20, video_to_start_from=None):
    videos = Video.all().order_by('-id').prefetch_related('author', 'preview')
    if video_to_start_from is not None:
        videos = videos.filter(id__lt=video_to_start_from.id)
    return await videos.limit(count)


async def get_video_previews_count():
    return await VideoPreview.all().count()


async def get_videos_count():
    return await Video.all().count()

