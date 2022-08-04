from typing import List

from utils import get_event_loop

from .lib.models import Video
from .lib.video_list_parser import VideoListParser
from .lib.proxier import FreeProxier as Proxier
from .lib.paginator import Paginator
from .lib.downloader import download_videos


async def _get_videos_list(url: str) -> List[Video]:
    parser = VideoListParser()
    return await parser.get_videos(url)


async def _init_database(app):
    from src.lib.database import init_database
    await init_database(app)


async def _crowl(app):
    await _init_database(app)
    url = app.ctx.config.CROWLING_URL
    root = app.ctx.config.CROWLING_ROOT

    paginator = Paginator(url)
    proxier = Proxier()
    for url in paginator.get_urls_iter():
        videos = await _get_videos_list(url)
        await download_videos(root, videos, proxier)


def crowl(app):
    loop = get_event_loop()
    loop.run_until_complete(_crowl(app))
