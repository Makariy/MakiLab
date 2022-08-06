import importlib
import inspect
import asyncio
from typing import List

from sanic import Sanic
from asyncio import AbstractEventLoop

from tortoise import Model
from tortoise.exceptions import ConfigurationError

from utils import get_event_loop

from .test import TestCase, TestFailedException
from lib.models import BaseModel

import colorama
colorama.init()


class _TestQueue:
    def __init__(self):
        self.errors_queue = []

    def add_error(self, error: Exception):
        self.errors_queue.append(error)

    def get_errors(self):
        return self.errors_queue


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

    async def _run_test(self, func):
        """Runs a test"""
        await func()

    async def _run_class_tests(self, cls: TestCase.__class__) -> _TestQueue:
        """Runs all the class tests"""
        test_queue = _TestQueue()

        test_class = cls(self.app)
        await test_class.setUp()

        funcs = dir(test_class)
        for func_name in funcs:
            func = getattr(test_class, func_name)
            if func_name.startswith('test_') and asyncio.iscoroutinefunction(func):
                try:
                    await self._run_test(func)
                    print(f'\t\tTest {func_name} is completed')
                except TestFailedException as e:
                    test_queue.add_error(e)
                    print(colorama.Fore.RED + f"\t\tTest {func_name} failed with error: \n{'='*20} {e} \n{'='*20}\n" +
                          colorama.Fore.RESET)
                except Exception as e:
                    print(colorama.Fore.RED + f"\t\tAn error: {e} occured in {func_name} test" + colorama.Fore.RESET)
        return test_queue

    async def _run_module_test_classes(self, module_name: str) -> List[Exception]:
        """Runs all the module test classes"""
        all_errors = []
        for test_class in self._get_module_classes_by_base_class(module_name, TestCase):
            test_queue = await self._run_class_tests(test_class)
            errors = test_queue.get_errors()
            print((colorama.Fore.GREEN if len(errors) == 0 else colorama.Fore.RED) +
                  f'\tAll {test_class} tests are completed with {len(errors)} errors' +
                  colorama.Fore.RESET)
            if len(errors) > 0:
                all_errors.append(*errors)

        return all_errors

    async def _run_all_tests(self):
        """Runs all the tests"""
        try:
            for app in self.config.INSTALLED_APPS:
                try:
                    errors = await self._run_module_test_classes(app + '.test')
                    print((colorama.Fore.GREEN if len(errors) == 0 else colorama.Fore.RED) +
                          f"All {app} tests are completed with {len(errors)} errors\n" +
                          "-"*20 + colorama.Fore.RESET)
                except Exception as e:
                    print(colorama.Fore.RED + f"An error occurred during trying to run {app} tests: {e}")
        finally:
            # Clean up
            await self._clean_up()

    async def _clean_up(self):
        """Cleans up the database after testing"""

        for module in self.config.INSTALLED_APPS:
            classes = self._get_module_classes_by_base_class(f'{module}.models', Model)
            for cls in classes:
                if cls.__name__ not in (BaseModel.__name__, Model.__name__):
                    try:
                        await cls.all().delete()
                    except ConfigurationError as e:
                        print(colorama.Fore.RED + f"An exception occurred trying to cleanup '{cls}': {e}")

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

