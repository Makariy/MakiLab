import importlib
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

    def _add_testing_task(self, app: Sanic, loop):
        """Adds a test task to sanic application loop"""
        loop.create_task(self._run_all_tests(app))

    async def _run_test(self, cls, func):
        """Runs a test"""
        await func()

    async def _run_class_tests(self, cls):
        """Runs all the class tests"""
        test_class = cls()
        await test_class.setUp()
        funcs = dir(test_class)
        for func in funcs:
            if func.startswith('test_'):
                await self._run_test(test_class, getattr(test_class, func))

    async def _run_module_test_classes(self, module_name):
        """Runs all the module test classes"""
        for test_class in self._get_module_classes_by_base_class(module_name, TestCase):
            await self._run_class_tests(test_class)

    async def _run_all_tests(self, app):
        """Runs all the tests"""
        self.app = app
        for app in self.config.INSTALLED_APPS:
            await self._run_module_test_classes(app + '.tests')
            print(f'All {app} tests are completed without any error')

        import asyncio
        for task in asyncio.Task.all_tasks():
            if task != asyncio.Task.current_task():
                task.cancel()

        await self.clean_up()
        self.app.stop()

    def setup_config(self, config):
        """Sets up the configuration settings"""
        self.config = config
        self.config.TESTING = True
        self.config.DB_NAME = 'test_' + self.config.DB_NAME
        self.config.app_events['after_server_start'].append(self._add_testing_task)

    async def clean_up(self):
        """Cleans up the database after testing"""
        for module in [*self.config.INSTALLED_APPS, 'lib']:
            classes = self._get_module_classes_by_base_class(f'{module}.models', Model)
            for cls in classes:
                if cls not in (BaseModel, Model):
                    await cls.all().delete()

    def run(self, run_app_func, config, args):
        """Runs the Tester which tests the application ran by
        function run_app_func with <config> and <args>"""
        self.setup_config(config)
        run_app_func('localhost', 8000, 1, self.config)