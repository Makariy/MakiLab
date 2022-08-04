from typing import Dict, List
from tortoise.functions import F

from auth.cache_models import Session
from videos.models import Video
from auth.models import User

from lib.cache.cache import Cache


async def was_video_watched(video: Video, session: Session) -> bool:
    if str(video.uuid) in session.context.watched:
        return True
    return False


async def add_is_videos_watched(
        videos: Dict[str, List[Dict[str, Dict[str, str]]]],
        user: User,
        session: Session
) -> Dict[str, List[Dict[str, Dict[str, str]]]]:
    for video in videos['videos']:
        if video['video']['uuid'] in session.context.watched:
            video['video']['watched'] = True
        else:
            video['video']['watched'] = False
    return videos


async def increment_views(video: Video, user: User, session: Session) -> bool:
    if not await was_video_watched(video, session):
        session.context.watched.append(video.uuid)
        await Cache.set(str(session.session_uuid), session.json())
        await Video.filter(uuid=video.uuid).update(views=F('views')+1)
        return True
    return False

