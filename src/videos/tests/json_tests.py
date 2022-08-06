from lib.tests import TestCase

from auth.models import User
from videos.models import Video

from videos.services.json_services import render_video, render_videos


class TestJsonServices(TestCase):
    async def setUp(self):
        self.author = await User.create_user("TestUser", "TestUserPassword")
        self.videos = [
            await Video.create(
                author=self.author,
                title=f"Test video {i}",
                description=f"Test video description {i}",
                file_name=f"testvideo{i}.mp4",
                preview=f"testvideo{i}.png",
                views=1 + i,
                real_url=f"http://realurl.com/{i}"
            ) for i in range(3)
        ]
        self.video = self.videos[0]
        self.rendered_video = {
            'video': {
                'author_name': self.video.author.username,
                'author_uuid': str(self.video.author.uuid),
                'title': self.video.title,
                'description': self.video.description,
                'video': self.video.file_name,
                'preview': self.video.preview,
                'views': self.video.views,
                'uuid': str(self.video.uuid)
            }
        }

    async def test_render_video(self):
        self.assertDictEqual(self.rendered_video, (await render_video(self.video)))

    async def test_render_videos(self):
        self.assertDictEqual(self.rendered_video, (await render_videos([self.video]))['videos'][0])


