import asyncio

from .lib.video_list_parser import VideoListParser
from .lib.proxier import Proxier
from .lib.paginator import Paginator
from .lib.downloader import download_videos


def get_loop():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    return loop


def get_videos_list(url: str):
    loop = get_loop()
    parser = VideoListParser(url)
    return loop.run_until_complete(parser.get_videos())


def init_database(app):
    from lib.database import init_database
    loop = get_loop()
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
    # Save used proxies
    del proxier

