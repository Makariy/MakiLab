import os
import ffmpeg
import aiohttp

from typing import List

from utils import get_event_loop
from ... import config
from .proxier import Proxier
from .video_page_parser import VideoPageParser
from .models import HLS, Video, Proxy
from .exceptions import VideoPageHasNoHLSLinkException
from src.videos.services.extern_services import create_preview


async def _get_video_hls(video: Video, proxy: Proxy):
    parser = VideoPageParser()
    return await parser.get_video_hls(video, proxy)


async def _download_preview(video: Video):
    async with aiohttp.ClientSession() as session:
        response = await session.get(video.preview_url)
        preview = await create_preview(await response.content.read())
        return preview


async def _download_video(video: Video, hls: HLS, proxy: Proxy) -> Video:
    from src.videos.models import Video as DBVideo
    from src.lib.models import User
    from src.videos.services.db_services import get_video_by_params

    downloaded_video = await get_video_by_params(real_url=video.url)
    if downloaded_video is not None:
        print(f'Already downloaded {video.title}({downloaded_video.file_name})')
        return downloaded_video

    file_name = video.uuid
    save_path = os.path.join(config.VIDEO_SAVING_PATH, file_name)
    command = ffmpeg \
        .input(hls.url, http_proxy=str(proxy)) \
        .output(save_path,
                f='mp4', codec='copy', loglevel='error')

    print(f'Downloading video: {video.title} ({video.uuid})')
    command.run()

    preview_file_name = await _download_preview(video)
    author = await User.get(id=1)
    video = await DBVideo.create(
        author=author,
        title=video.title,
        description=video.title + ' description',
        file_name=file_name,
        preview=preview_file_name,
        views=0,
        real_url=video.url
    )
    return video


def download_videos(root: str, videos: List[Video], proxier: Proxier):
    loop = get_event_loop()
    proxy = proxier.get_proxy()

    for video in videos:
        video.url = root + video.url

        try:
            hls = loop.run_until_complete(_get_video_hls(video, proxy))
            db_video = loop.run_until_complete(_download_video(video, hls, proxy))
            if db_video:
                print(f'\tDownloaded video: {video.title}')

        except ffmpeg.Error:
            proxier.add_used_proxy(proxy)
            proxy = proxier.get_proxy()
        except VideoPageHasNoHLSLinkException:
            print(f'Cannot download video: {video.title} because it has no HLS link')


