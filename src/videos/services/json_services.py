from typing import List, Dict, Literal
from videos.models import Video  # type


async def render_video(video: Video) -> Dict[Literal['video'], Dict[str, str]]:
    return {
        'video': {
            'title': video.title,
            'description': video.description,
            'views': video.views,
            'video': video.file_name,
            'preview': video.preview,
            'uuid': str(video.uuid),
            'author_name': video.author.username,
            'author_uuid': str(video.author.uuid)
        }
    }


async def render_videos(videos: List[Video]) -> Dict[Literal['videos'], List[Dict[Literal['video'], Dict[str, str]]]]:
    return {
        'videos': [await render_video(video) for video in videos]
    }
