from typing import Tuple
from src.videos.models import Video


async def render_video(video: Video):
    return {
        'video': {
            'title': video.title,
            'description': video.description,
            'views': video.views,
            'preview': str(video.preview.uuid),
            'uuid': str(video.uuid),
            'author_name': video.author.username,
            'author_uuid': str(video.author.uuid)
        }
    }


async def render_videos(videos: Tuple[Video]):
    return {
        'videos': [await render_video(video) for video in videos]
    }
