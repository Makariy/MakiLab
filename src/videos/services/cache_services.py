from tortoise.functions import F

from auth.cache_models import Session
from videos.models import Video
from auth.models import User

from lib.cache.cache import Cache


async def increment_views(video: Video, user: User, session: Session) -> bool:
    watched_videos = session.context.get("watched")
    if watched_videos is None:
        watched_videos = session.context['watched'] = []

    if str(video.uuid) not in watched_videos:
        await Video.filter(uuid=video.uuid).update(views=F('views')+1)

        session.context['watched'].append(video.uuid)
        await Cache.set(str(session.session_uuid), session.json())
        return True
    return False

