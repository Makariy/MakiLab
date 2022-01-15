from typing import List, Dict
from src.videos.models import Video


async def render_video(video: Video) -> Dict[str, Dict[str, str]]:
    return {
        'video': {
            'title': video.title,
            'description': video.description,
            'views': video.views,
            'preview': str(video.preview.file_name),
            'uuid': str(video.uuid),
            'author_name': video.author.username,
            'author_uuid': str(video.author.uuid)
        }
    }


async def render_videos(videos: List[Video]) -> Dict[str, List[Dict[str, Dict[str, str]]]]:
    return {
        'videos': [await render_video(video) for video in videos]
    }
