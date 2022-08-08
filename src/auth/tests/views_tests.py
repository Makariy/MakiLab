from lib.tests import TestCase

from auth.models import User


class TestViews(TestCase):
    async def setUp(self):
        self.username = "TestUser"
        self.password = "TestUserPassword"
        self.user = await User.create_user(self.username, self.password)

    async def test_login_view(self):
        client = self.get_client()
        async with client.create_session() as session:
            response = await client.post(session, 'auth/login/', data={
                'username': self.username,
                'password': self.password
            })
            self.assertEquals(response.status, 200)
            self.assertNotEquals(response.cookies.get('session_uuid'), None)
            response = await response.json()
            self.assertEquals(response.get('status'), 'success')

    async def test_logout_view(self):
        client = self.get_client()
        async with client.create_session() as session:
            await client.post(session, 'auth/login/', data={
                'username': self.username,
                'password': self.password
            })
            response = await client.post(session, 'auth/logout/')
            self.assertEquals(response.status, 200)
            self.assertEquals(response.cookies.get('session_uuid').value, "")
            response = await response.json()
            self.assertEquals(response.get('status'), 'success')

    async def test_signup_view(self):
        client = self.get_client()
        async with client.create_session() as session:
            response = await client.post(session, 'auth/signup/', data={
                'username': 'NewUser',
                'password': 'NewUserPassword'
            })
            self.assertEquals(response.status, 200)
            self.assertNotEquals(response.cookies.get("session_uuid"), None)
            response = await response.json()
            self.assertEquals(response.get('status'), 'success')
