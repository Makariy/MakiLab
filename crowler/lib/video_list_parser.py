import aiohttp
from uuid import uuid4
from typing import List, Dict
from bs4 import BeautifulSoup as Soup


class VideoListParser:
    def __init__(self, url):
        self.url = url

    async def _make_soup(self):
        async with aiohttp.ClientSession() as session:
            response = await session.get(self.url)
            return Soup(await response.text())

    async def _get_video_title(self, html_video: Soup):
        return html_video.find(**{'class': 'title'}).findChild().get_attribute_list('title')[0]

    async def _get_video_preview_link(self, html_video: Soup):
        return html_video.find(**{'id': lambda a: a and a.startswith('pic_')}).get_attribute_list('data-src')[0]

    async def _get_video_link(self, html_video: Soup):
        return html_video.find(**{'class': 'title'}).findChild().get_attribute_list('href')[0]

    async def _render_video(self, html_video: Soup) -> Dict[str, str]:
        return {
            'title': await self._get_video_title(html_video),
            'preview_link': await self._get_video_preview_link(html_video),
            'link': await self._get_video_link(html_video),
            'uuid': str(uuid4())
        }

    async def _render_videos(self, html_videos: List[Soup]) -> Dict[str, List[Dict[str, str]]]:
        videos = []
        for video in html_videos:
            videos.append(await self._render_video(video))
        return {
            'videos': videos
        }

    async def _get_videos(self, soup: Soup) -> Dict[str, List[Dict[str, str]]]:
        html_videos = soup.find_all(**{'id': lambda a: a and a.startswith('video_')})
        return await self._render_videos(html_videos)

    async def get_videos_rendered(self) -> Dict[str, List[Dict[str, str]]]:
        soup = await self._make_soup()
        return await self._get_videos(soup)


