from typing import List

from utils import get_event_loop

from .lib.models import Video
from .lib.video_list_parser import VideoListParser
from .lib.proxier import FreeProxier as Proxier
from .lib.paginator import Paginator
from .lib.downloader import download_videos


def get_videos_list(url: str) -> List[Video]:
    loop = get_event_loop()
    parser = VideoListParser()
    return loop.run_until_complete(parser.get_videos(url))


def init_database(app):
    from src.lib.database import init_database
    loop = get_event_loop()
    loop.run_until_complete(init_database(app, loop))


def crowl(app):
    init_database(app)
    url = app.ctx.config.CROWLING_URL
    root = app.ctx.config.CROWLING_ROOT

    paginator = Paginator(url)
    proxier = Proxier()
    for url in paginator.get_urls_iter():
        videos = get_videos_list(url)
        download_videos(root, videos, proxier)

