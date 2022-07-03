import importlib
import inspect
import asyncio

from sanic import Sanic
from asyncio import AbstractEventLoop

from tortoise import Model
from tortoise.exceptions import ConfigurationError

from utils import get_event_loop
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
        except ImportError as e:
            raise e
        for cls in dir(module):
            obj = getattr(module, cls)
            if inspect.isclass(obj):
                if issubclass(obj, base) and obj is not base:
                    ret.append(obj)
        return ret

    async def _run_test(self, cls, func):
        """Runs a test"""
        await func()

    async def _run_class_tests(self, cls: TestCase.__class__):
        """Runs all the class tests"""
        test_class = cls(self.app)
        await test_class.setUp()

        funcs = dir(test_class)
        for func_name in funcs:
            func = getattr(test_class, func_name)
            if func_name.startswith('test_') and asyncio.iscoroutinefunction(func):
                try:
                    await self._run_test(test_class, func)
                    print(f'\t\tTest {func_name} is completed')
                except Exception as e:
                    print(f"\t\tTest {func_name} failed with error: {e}")

    async def _run_module_test_classes(self, module_name: str):
        """Runs all the module test classes"""
        for test_class in self._get_module_classes_by_base_class(module_name, TestCase):
            await self._run_class_tests(test_class)
            print(f'\tAll {test_class} tests are completed without any error')

    async def _run_all_tests(self):
        """Runs all the tests"""
        try:
            for app in self.config.INSTALLED_APPS:
                try:
                    await self._run_module_test_classes(app + '.tests')
                    print(f"All {app} tests are completed without any error")
                except Exception as e:
                    print(f"An error occurred during trying to run {app} tests: {e}")
        finally:
            # Clean up
            await self._clean_up()

    async def _clean_up(self):
        """Cleans up the database after testing"""

        for module in ['lib', *self.config.INSTALLED_APPS]:
            classes = self._get_module_classes_by_base_class(f'{module}.models', Model)
            for cls in classes:
                if cls.__name__ not in (BaseModel.__name__, Model.__name__):
                    try:
                        await cls.all().delete()
                    except ConfigurationError as e:
                        print(f"An exception occurred trying to cleanup '{cls}': {e}")

    def _init_database(self, loop: AbstractEventLoop, app: Sanic):
        from src.lib.database import init_database
        loop.run_until_complete(init_database(self.app, None))

    def setup_config(self, config):
        """Sets up the configuration settings"""
        self.config = config
        self.config.TESTING = True
        self.config.DB_NAME = 'test_' + self.config.DB_NAME

    def run(self, app: Sanic, config, args):
        """Runs the Tester which tests the application <app>
         with <config> and <args>"""
        self.app = app
        self.setup_config(config)

        loop = get_event_loop()
        self._init_database(loop, app)
        loop.run_until_complete(self._run_all_tests())

