import os
import ffmpeg
import aiohttp

from typing import List, Union

import config

from .proxier import Proxier
from .video_page_parser import VideoPageParser
from .models import HLS, Video, Proxy
from .exceptions import VideoPageHasNoHLSLinkException

from auth.models import User
from videos.models import Video as DBVideo
from videos.services.db_services import get_video_by_params
from videos.services.extern_services import create_preview


async def _get_video_hls(video: Video, proxy: Proxy):
    parser = VideoPageParser()
    return await parser.get_video_hls(video, proxy)


async def _get_downloaded_video_from_db(video: Video) -> Union[DBVideo, None]:
    downloaded_video = await get_video_by_params(real_url=video.url)
    if downloaded_video is not None:
        return downloaded_video
    return None


async def _download_preview(video: Video):
    async with aiohttp.ClientSession() as session:
        response = await session.get(video.preview_url)
        preview = await create_preview(await response.content.read())
        return preview


async def _download_video_data(hls: HLS, output_path: str, proxy: Proxy):
    command = ffmpeg \
        .input(hls.url, http_proxy=str(proxy)) \
        .output(output_path,
                f='mp4', codec='copy', loglevel='error')
    command.run()


async def _download_video(video: Video, hls: HLS, proxy: Proxy) -> Video:
    existing_video = await _get_downloaded_video_from_db(video)
    if existing_video is not None:
        print(f'Already downloaded {video.title}({existing_video.file_name})')
        return existing_video

    file_name = video.uuid
    output_path = os.path.join(config.VIDEO_SAVING_PATH, file_name)
    print(f'Downloading video: {video.title} ({video.uuid})')

    await _download_video_data(hls, output_path, proxy)
    preview_file_name = await _download_preview(video)
    author = await User.first()
    db_video = await DBVideo.create(
        author=author,
        title=video.title,
        description=video.title + ' description',
        file_name=file_name,
        preview=preview_file_name,
        views=0,
        real_url=video.url
    )
    print(f'[{video.uuid}] Done')
    return db_video


async def download_videos(root: str, videos: List[Video], proxier: Proxier):
    proxy = proxier.get_proxy()

    for video in videos:
        video.url = root + video.url
        try:
            hls = await _get_video_hls(video, proxy)
            db_video = await _download_video(video, hls, proxy)

        except ffmpeg.Error:
            proxier.add_used_proxy(proxy)
            proxy = proxier.get_proxy()
        except VideoPageHasNoHLSLinkException:
            print(f'Cannot download video: {video.title} because it has no HLS link')


