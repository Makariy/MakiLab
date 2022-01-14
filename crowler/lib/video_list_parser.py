import aiohttp
from uuid import uuid4
from typing import List
from bs4 import BeautifulSoup as Soup
from .models import Video


class VideoListParser:
    def __init__(self, url):
        self.url = url

    async def _make_soup(self):
        async with aiohttp.ClientSession() as session:
            response = await session.get(self.url)
            return Soup(await response.text(), 'html.parser')

    async def _get_video_title(self, html_video: Soup):
        return html_video.find(**{'class': 'title'}).findChild().get_attribute_list('title')[0]

    async def _get_video_preview_link(self, html_video: Soup):
        return html_video.find(**{'id': lambda a: a and a.startswith('pic_')}).get_attribute_list('data-src')[0]

    async def _get_video_link(self, html_video: Soup):
        return html_video.find(**{'class': 'title'}).findChild().get_attribute_list('href')[0]

    async def get_videos(self) -> List[Video]:
        soup = await self._make_soup()
        html_videos = soup.find_all(**{'id': lambda a: a and a.startswith('video_')})
        videos = []
        for html_video in html_videos:
            videos.append(Video(
                title=await self._get_video_title(html_video),
                url=await self._get_video_link(html_video),
                preview_url=await self._get_video_preview_link(html_video),
                uuid=str(uuid4())
            ))
        return videos


