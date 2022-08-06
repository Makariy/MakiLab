import uuid
from lib.tests import TestCase
from auth.models import User
from videos.models import Video

from src.videos.services.db_services import get_video_by_params
from src.videos.services.db_services import get_videos
from src.videos.services.db_services import get_videos_count


class TestDatabaseServices(TestCase):
    async def setUp(self):
        self.user = await User.create_user('TestUser', 'TestUserPassword')
        self.videos = []
        for i in range(10):
            self.videos.append(await Video.create(
                author=self.user,
                title=f'Test video {i}',
                description=f'Test video description {i}',
                file_name=f'test_video_{i}.mp4',
                preview=uuid.uuid4(),
            ))

    async def test_get_video(self):
        test_video = self.videos[0]
        video = await get_video_by_params(id=test_video.id)
        self.assertEquals(video, test_video)

    async def test_get_videos_count(self):
        videos_count = await get_videos_count()
        self.assertEquals(videos_count, len(self.videos))

    async def test_get_videos(self):
        videos = await get_videos(count=len(self.videos))
        self.assertEquals(videos, self.videos[::-1])

    async def test_get_videos_with_offset(self):
        video_to_start_from = self.videos[len(self.videos) // 2]
        videos = await get_videos(video_to_start_from=video_to_start_from)
        index = self.videos.index(video_to_start_from)
        self.assertEquals(videos, self.videos[index-1::-1])

