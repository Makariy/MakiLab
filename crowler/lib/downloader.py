import os
import ffmpeg
import asyncio
import aiohttp
from typing import List

import config
from .proxier import Proxier
from .video_page_parser import VideoPageParser
from .models import HLS, Video, Proxy
from .exceptions import VideoPageHasNoHLSLinkException, NoMoreProxiesException
from src.videos.services.extern_services import create_preview


def _get_loop():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    return loop


def _get_video_hls(video: Video, proxy: Proxy):
    loop = _get_loop()
    parser = VideoPageParser()
    return loop.run_until_complete(parser.get_video_hls(video, proxy))


async def _download_preview(video: Video):
    async with aiohttp.ClientSession() as session:
        response = await session.get(video.preview_url)
        preview = await create_preview(await response.content.read())
        return preview


async def _download_video(video: Video, hls: HLS, proxy: Proxy):
    from src.videos.models import Video as DBVideo
    from lib.models import User
    from src.videos.services.db_services import get_video_by_params

    downloaded_video = await get_video_by_params(real_url=video.url)
    if downloaded_video is not None:
        print(f'Already downloaded {downloaded_video.title}({downloaded_video.file_name})')
        return False

    file_name = video.uuid
    save_path = os.path.join(config.VIDEO_SAVING_PATH, file_name)
    command = ffmpeg \
        .input(hls.url, http_proxy=str(proxy)) \
        .output(save_path,
                f='mp4', codec='copy', loglevel='error')

    print(f'Downloading video: {video.title} ({video.uuid})')
    command.run()

    preview = await _download_preview(video)
    await DBVideo.create(
        author=await User.get(id=1),
        title=video.title,
        description=video.title + ' description',
        file_name=file_name,
        preview=preview,
        views=0,
        real_url=video.url
    )
    print(f'\tDownloaded video: {video.title}')
    return True


def download_videos(root: str, videos: List[Video], proxier: Proxier):
    loop = _get_loop()
    proxy = proxier.get_proxy()

    for video in videos:
        video.url = root + video.url

        try:
            hls = _get_video_hls(video, proxy)
            loop.run_until_complete(_download_video(video, hls, proxy))
        except ffmpeg.Error:
            proxier.add_used_proxy(proxy)
            proxy = proxier.get_proxy()
        except VideoPageHasNoHLSLinkException:
            print(f'Cannot download video: {video.title} because it has no HLS link')


