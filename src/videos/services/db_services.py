from tortoise.exceptions import DoesNotExist
from videos.models import Video


async def get_video_by_params(prefetch_author=False, **params):
    try:
        video = Video.get(**params)
        if prefetch_author:
            video = video.prefetch_related('author')
        return await video
    except DoesNotExist:
        return None


async def get_videos(prefetch_author=False, count=20, page=1, video_to_start_from=None):
    videos = Video.all().order_by('-id').offset((page - 1) * count)
    if prefetch_author:
        videos = videos.prefetch_related('author')
    if video_to_start_from is not None:
        videos = videos.filter(id__lt=video_to_start_from.id)
    return await videos.limit(count)


async def get_videos_count():
    return await Video.all().count()

