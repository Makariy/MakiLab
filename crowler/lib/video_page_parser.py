import re
import os
from bs4 import BeautifulSoup as Soup
from typing import List, Dict
import aiohttp
import ffmpeg
from .proxier import Proxy


class HLS:
    def __init__(self, name, resolution, bandwidth, url):
        self.name = name
        self.resolution = resolution
        self.bandwidth = bandwidth
        self.url = url

    name: str
    resolution: str
    bandwidth: int
    url: str


class QUALITY:
    BEST = 1
    NORMAL = 2
    WORST = 3


class VideoPageParser:
    async def _make_soup(self, url) -> Soup:
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            return Soup(await response.text(), 'html.parser')

    async def _get_video_hls_url(self, soup: Soup) -> str:
        return re.compile(r"(?<=setVideoHLS\(['\"]).+(?=['\"]\))").findall(str(soup))[0]

    async def _parse_video_hls(self, hls_url: str) -> List[HLS]:
        prefix = "/".join(hls_url.split("/")[:-1]) + '/'
        hlss = []
        hls_data = str(await self._make_soup(hls_url))
        lines = hls_data.strip().split('\n')
        for idx, line in enumerate(lines):
            if idx % 2 == 1:
                data_line = line.split(':')[-1]
                data = {attrib.split('=')[0]: attrib.split('=')[1] for attrib in data_line.split(',')}
                hlss.append(HLS(
                    name=data['NAME'],
                    bandwidth=data['BANDWIDTH'],
                    resolution=data['RESOLUTION'],
                    url=prefix + lines[idx + 1].replace('&amp;', '&')
                ))
        return sorted(hlss, key=lambda x: int(x.bandwidth))

    async def _get_video_hls(self, video_url: str, quality: QUALITY = QUALITY.NORMAL):
        video_html = await self._make_soup(video_url)
        hls_url = await self._get_video_hls_url(video_html)
        hls_list = await self._parse_video_hls(hls_url)

        if quality == QUALITY.BEST:
            return hls_list[-1]
        elif quality == QUALITY.NORMAL:
            if len(hls_list) > 2:
                return hls_list[len(hls_list) - 2]
            return hls_list[len(hls_list) // 2]
        else:
            return hls_list[0]

    async def download_video(self, video: Dict[str, str], proxy: Proxy, directory='data'):
        try:
            hls = await self._get_video_hls(video['url'])
            command = ffmpeg\
                .input(hls.url, http_proxy=f'https://{proxy.ip}:{proxy.port}/')\
                .output(os.path.join(directory, video['uuid'] + '.mp4'),
                                         codec='copy', loglevel='error')

            print(f'Downloading video: {video["title"]}')
            command.run()
            print(f'\t\tDownloaded video: {video["title"]}')
        except:
            print(f'Cannot download video: {video["title"]}')
            raise RuntimeError('Connection refused')
