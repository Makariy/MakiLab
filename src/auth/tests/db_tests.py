from lib.tests import TestCase

from auth.models import User
from auth.services.db_services import get_user_by_params, create_user


class TestDBServices(TestCase):
    async def setUp(self):
        self.user = await User.create_user("TestUser", "TestUserPassword")

    async def test_get_user_by_params(self):
        self.assertEquals(self.user, await get_user_by_params(uuid=self.user.uuid))

    async def test_create_user(self):
        user, error = await create_user("NewUser", "NewUserPassword")
        self.assertEquals(error, None)
        self.assertNotEquals(user, None)
