from pypika import CustomFunction
from tortoise.functions import Function
from tortoise.exceptions import DoesNotExist
from videos.models import Video


class TrigramSearch(Function):
    database_func = CustomFunction("similarity", ["title", "query"])


async def get_video_by_params(prefetch_author=True, **params):
    try:
        video = Video.get(**params)
        if prefetch_author:
            video = video.prefetch_related('author')
        return await video
    except DoesNotExist:
        return None


async def get_videos(prefetch_author=True, count=20, page=1, video_to_start_from=None):
    videos = Video.all().order_by('-id').offset((page - 1) * count)
    if prefetch_author:
        videos = videos.prefetch_related('author')
    if video_to_start_from is not None:
        videos = videos.filter(id__lt=video_to_start_from.id)
    return await videos.limit(count)


async def search_videos(query="", prefetch_author=True, count=20, page=1):
    videos = Video.all().annotate(similarity=TrigramSearch("title", query)).order_by('-similarity')
    if prefetch_author:
        videos = videos.prefetch_related("author")

    return await videos.limit(count*page)


async def get_videos_count():
    return await Video.all().count()

