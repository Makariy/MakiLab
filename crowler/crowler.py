import asyncio
from .lib.video_list_parser import VideoListParser


url = 'https://xvideos.com/'


def get_videos_list():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()

    parser = VideoListParser(url)
    return loop.run_until_complete(parser.get_videos_rendered())

