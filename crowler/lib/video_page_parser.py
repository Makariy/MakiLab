import re
from bs4 import BeautifulSoup as Soup
from typing import List
import aiohttp
from .models import Video, HLS, QUALITY
from .exceptions import VideoPageHasNoHLSLinkException


class VideoPageParser:
    async def _make_soup(self, url) -> Soup:
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            return Soup(await response.text(), 'html.parser')

    async def _get_video_hls_url(self, soup: Soup) -> str:
        hls_url = re.compile(r"(?<=setVideoHLS\(['\"]).+(?=['\"]\))").findall(str(soup))
        if len(hls_url) == 0:
            raise VideoPageHasNoHLSLinkException()

        return hls_url[0]

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

    async def get_video_hls(self, video: Video, quality: QUALITY = QUALITY.NORMAL):
        video_html = await self._make_soup(video.url)
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


