import aiohttp
from typing import Dict


class TestFailedException(Exception):
    def __init__(self, msg=''):
        super().__init__(msg)


class TestClient:
    def __init__(self, config):
        self.host = f"{config.HOST}:{config.PORT}"

    def create_session(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession()

    async def get(self, session: aiohttp.ClientSession, path: str) -> aiohttp.ClientResponse:
        response = await session.get(f"http://{self.host}/{path}")
        return response

    async def post(self, session: aiohttp.ClientSession, path: str, data: Dict) -> aiohttp.ClientResponse:
        response = await session.post(f"http://{self.host}/{path}", data=data)
        return response


class TestCase:
    def __init__(self, app):
        self.app = app

    def get_client(self):
        return TestClient(self.app.ctx.config)

    async def setUp(self):
        """Initialize all the class variables"""
        pass

    def assertEquals(self, first, second, **kwargs):
        """Asserts that first == second"""
        if first != second:
            raise TestFailedException((kwargs.get('msg') or '') +
                                            f'\nError during assertEquals: {first} != {second}')

    def assertNotEquals(self, first, second, **kwargs):
        """Asserts that first != second"""
        if first == second:
            raise TestFailedException((kwargs.get('msg') or '') +
                                            f'\nError during assertNotEquals: {first} == {second}')

    def assertTrue(self, value, **kwargs):
        """Asserts that value is not True"""
        if value is not True:
            raise TestFailedException((kwargs.get('msg') or '') +
                                            f'\nError during assertTrue: {value} is not True')

    def assertRaises(self, func, exc: Exception, **kwargs):
        """Asserts that function raises an exception exc"""
        try:
            func()
        except Exception as e:
            if not isinstance(e, exc.__class__):
                raise TestFailedException(f'Error during assertRaises: {func} '
                                          f'had not raised an exception of type {exc.__class__}')
            return

        raise TestFailedException((kwargs.get('msg') or '') +
                                            f'\nError during assertRaises: {func}'
                                            f'had not raised an exception')

    def assertDictEqual(self, dict1, dict2, **kwargs):
        """Asserts that dict1 contains the same keys as dict2 and that it values are equal"""
        for key in dict1:
            if key not in dict2:
                raise TestFailedException((kwargs.get('msg') or '') +
                                            f'\nError during assertDictEqual: {dict1} and {dict2}\n'
                                            f'dict2 does not contain "{key}", which is present in dict1')
            if type(dict1[key]) is dict:
                self.assertDictEqual(dict1[key], dict2[key])

        for key in dict2:
            if key not in dict1:
                raise TestFailedException((kwargs.get('msg') or '') +
                                          f'\nError during assertDictEqual: {dict2} and {dict1}\n'
                                          f'dict1 does not contain "{key}", which is present in dict2')
            if type(dict2[key]) is dict:
                self.assertDictEqual(dict2[key], dict1[key])

        keys = {*dict1.keys(), *dict2.keys()}
        for key in keys:
            if dict1[key] != dict2[key]:
                raise TestFailedException((kwargs.get('msg') or '') +
                                          f'\nError during assertDictEqual: {dict1} and {dict2}\n'
                                          f'dict1["{key}"] != dict2["{key}"],\n'
                                          f'{dict1[key]} != {dict2[key]}')


