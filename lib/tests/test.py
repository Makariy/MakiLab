
class TestFailedException(Exception):
    def __init__(self, msg=''):
        super().__init__(msg)


class TestCase:
    async def startUp(self):
        pass

    def assertEquals(self, first, second, **kwargs):
        if first != second:
            raise TestFailedException((kwargs.get('msg') or '') +
                                            f'\nError during assertEquals: {first} != {second}')

    def assertNotEquals(self, first, second, **kwargs):
        if first == second:
            raise TestFailedException((kwargs.get('msg') or '') +
                                            f'\nError during assertNotEquals: {first} == {second}')

    def assertTrue(self, value, **kwargs):
        if value is not True:
            raise TestFailedException((kwargs.get('msg') or '') +
                                            f'\nError during assertTrue: {value} is not True')

    def assertRaises(self, func, exc: Exception, **kwargs):
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

