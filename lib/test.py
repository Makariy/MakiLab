import os
from aiohttp.client import ClientSession
from sanic import Sanic


class TestFailedException(Exception):
    def __init__(self, msg=''):
        super().__init__(msg)


class TestCase:
    async def startUp(self):
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
                                            f'\nError during assertDictEqual: {dict1} and {dict2} '
                                            f'dict1.keys() does not contain all dict2.keys()')

            if dict1[key] != dict2[key]:
                raise TestFailedException((kwargs.get('msg') or '') +
                                            f'\nError during assertDictEqual: {dict1} and {dict2} '
                                            f'dict1[{key}] != dict2[{key}], '
                                            f'{dict1[key]} != {dict2[key]}')

