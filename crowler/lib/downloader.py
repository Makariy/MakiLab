import os
import ffmpeg
import asyncio
from typing import List
from .proxier import Proxier
from .video_page_parser import VideoPageParser
from .models import HLS, Video, Proxy


def _get_loop():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    return loop


def _get_video_hls(video: Video):
    loop = _get_loop()
    parser = VideoPageParser()
    return loop.run_until_complete(parser.get_video_hls(video))


async def _download_video(video: Video, hls: HLS, proxy: Proxy, directory: str):
    from src.videos.models import Video as DBVideo
    from src.videos.models import VideoPreview
    from lib.models import User

    path = os.path.join(directory, video.uuid)
    command = ffmpeg \
        .input(hls.url, http_proxy=f'https://{proxy.ip}:{proxy.port}/') \
        .output(path,
                codec='copy', loglevel='error')

    print(f'Downloading video: {video.title} ({video.uuid})')
    command.run()

    preview = await VideoPreview.create(file_name=video.preview_url)
    await DBVideo.create(
        author=await User.get(id=1),
        title=video.title,
        description=video.title + ' description',
        file_name=path,
        preview=preview,
        views=0
    )
    print(f'\t\tDownloaded video: {video.title}')


def download_videos(root: str, videos: List[Video], proxier: Proxier):
    proxies = proxier.get_proxies()
    proxies_count = len(proxies)

    loop = _get_loop()

    for i in range(0, len(videos), proxies_count):
        videos_set = videos[i:i+proxies_count]
        for x in range(len(videos_set)):
            video = videos_set[x]
            video.url = root + video.url
            hls = _get_video_hls(video)

            try:
                loop.run_until_complete(_download_video(video, hls, proxies[x], '/home/makariy/disk/data/'))
            except ffmpeg.Error:
                proxies = proxier.get_proxies(8)


