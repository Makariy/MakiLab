import importlib
import asyncio
from sanic import Sanic
from tortoise import Model

from lib.test import TestCase
from lib.models import BaseModel


class Tester:
    config = None
    app = None

    def _get_module_classes_by_base_class(self, module_name, base):
        """Runs all the module test classes"""
        ret = []
        try:
            module = importlib.import_module(module_name)
            for cls in dir(module):
                obj = getattr(module, cls)
                try:
                    if issubclass(obj, base):
                        ret.append(obj)
                except TypeError:
                    pass
        except ImportError as e:
            print(e)
        return ret

    async def _run_test(self, cls, func):
        """Runs a test"""
        await func()

    async def _run_class_tests(self, cls):
        """Runs all the class tests"""
        test_class = cls(self.app)
        await test_class.setUp()
        funcs = dir(test_class)
        for func_name in funcs:
            func = getattr(test_class, func_name)
            if func_name.startswith('test_') and asyncio.iscoroutinefunction(func):
                await self._run_test(test_class, func)
                print(f'\t\tTest {func_name} is completed')

    async def _run_module_test_classes(self, module_name):
        """Runs all the module test classes"""
        for test_class in self._get_module_classes_by_base_class(module_name, TestCase):
            await self._run_class_tests(test_class)
            print(f'\tAll {test_class} tests are completed without any error')

    async def _run_all_tests(self):
        """Runs all the tests"""
        # Initialize the database
        from lib.database import init_database
        await init_database(self.app, None)

        for app in self.config.INSTALLED_APPS:
            await self._run_module_test_classes(app + '.tests')
            print(f'All {app} tests are completed without any error')

        # Clean up
        await self.clean_up()

    async def clean_up(self):
        """Cleans up the database after testing"""

        for module in ['lib', *self.config.INSTALLED_APPS]:
            classes = self._get_module_classes_by_base_class(f'{module}.models', Model)
            for cls in classes:
                if cls not in (BaseModel, Model):
                    await cls.all().delete()

    def setup_config(self, config):
        """Sets up the configuration settings"""
        self.config = config
        self.config.TESTING = True
        self.config.DB_NAME = 'test_' + self.config.DB_NAME

    def run(self, app, config, args):
        """Runs the Tester which tests the application <app>
         with <config> and <args>"""
        self.app = app
        self.setup_config(config)

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
        loop.run_until_complete(self._run_all_tests())

