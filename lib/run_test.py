import importlib
import config
from lib.tests.test import TestCase


class Tester:
    async def _run_test(self, cls, func):
        await func()

    async def _run_class_tests(self, cls):
        test_class = cls()
        await test_class.startUp()
        funcs = dir(test_class)
        for func in funcs:
            if func.startswith('test_'):
                await self._run_test(test_class, getattr(test_class, func))

    async def run_module_test_classes(self, module_name):
        module = importlib.import_module(module_name)
        for cls in dir(module):
            obj = getattr(module, cls)
            if obj.__class__ == type and issubclass(obj, TestCase):
                await self._run_class_tests(obj)

    async def run_all_tests(self, app, loop):
        for app in config.INSTALLED_APPS:
            await self.run_module_test_classes(app + '.tests')
