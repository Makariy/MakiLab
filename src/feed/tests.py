from lib.test import TestCase
from src.feed.models import User, FeedPostLike


class TestDBServices(TestCase):
    async def startUp(self):
        self.user = await User.create_user(username='Makar', password='Makariy123')
        await super().startUp()

    async def test_i_can_print(self):
        self.assertEquals(self.user, await User.get(id=self.user.id), msg=f'User with {self.user.id} was not created')
        self.assertTrue(True, msg='This is just to test')
