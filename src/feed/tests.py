from lib.tests.test import TestCase
from src.feed.models import User


class TestDBServices(TestCase):
    async def startUp(self):
        print('Running the test')
        self.user = await User.create_user(username='Makar', password='Makariy123')
        await super().startUp()

    async def test_i_can_print(self):
        self.assertEquals(self.user, await User.get(id=self.user.id), msg=f'User with {self.user.id} was not created')
        self.assertTrue(False, msg='This is just to test')
