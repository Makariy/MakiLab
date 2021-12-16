import importlib
from lib.test import TestCase
from sanic import Sanic
from src.feed.models import *


class Tester:
    config = None
    app = None

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

    async def _run_all_tests(self):
        for app in self.config.INSTALLED_APPS:
            await self.run_module_test_classes(app + '.tests')

        import asyncio
        for task in asyncio.Task.all_tasks():
            if task != asyncio.Task.current_task():
                task.cancel()

        await self._clean_up()
        self.app.stop()

    def _add_testing_task(self, app: Sanic, loop):
        self.app = app
        loop.create_task(self._run_all_tests())

    def _setup(self, config):
        self.config = config
        self.config.DB_NAME = 'test_' + self.config.DB_NAME
        self.config.app_events['after_server_start'].append(self._add_testing_task)

    async def _clean_up(self):
        await User.all().delete()
        await FeedPost.all().delete()
        await FeedPostLike.all().delete()
        await FeedPostImage.all().delete()
        await FeedPostComment.all().delete()

    def run(self, run_app_func, config, args):
        self._setup(config)
        run_app_func('localhost', 8000, 1, self.config)
