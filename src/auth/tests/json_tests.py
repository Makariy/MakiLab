from lib.tests import TestCase

from auth.models import User
from auth.services.json_services import render_user


class TestJsonServices(TestCase):
    async def setUp(self):
        self.user = await User.create_user("TestUser", "TestUserPassword")

    async def test_render_user(self):
        rendered_user = {
            'user': {
                "username": self.user.username,
                "uuid": str(self.user.uuid)
            }
        }
        self.assertDictEqual(rendered_user, (await render_user(self.user)))

    async def test_request_login_view(self):
        client = self.get_client()
        async with client.create_session() as session:
            response = await client.post(session, "auth/login/", data={
                "username": "TestUser",
                "password": "TestUserPassword"
            })
            self.assertEquals(response.status, 200)
