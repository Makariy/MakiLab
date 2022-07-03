from tortoise.exceptions import DoesNotExist

from videos.models import Video


async def get_video_by_params(**params):
    try:
        return await Video.get(**params).prefetch_related('author')
    except DoesNotExist:
        return None


async def get_last_videos(count=20, page=1, video_to_start_from=None):
    videos = Video.all().order_by('-id').prefetch_related('author').offset((page - 1) * count)
    if video_to_start_from is not None:
        videos = videos.filter(id__lt=video_to_start_from.id)
    return await videos.limit(count)


async def get_videos_count():
    return await Video.all().count()

