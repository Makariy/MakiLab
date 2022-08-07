from typing import List, Dict

import importlib
import inspect
import asyncio

from sanic import Sanic
from asyncio import AbstractEventLoop

from tortoise import Model
from tortoise.exceptions import ConfigurationError

from .test import TestCase, TestFailedException
from lib.models import BaseModel

from .test_queue import TestQueue
from .test_logger import TestLogger


class Tester:
    config = None
    app = None
    test_logger = TestLogger()

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

    async def _run_class_tests(self, cls: TestCase.__class__) -> TestQueue:
        """Runs all the class tests"""
        test_class = cls(self.app)
        await test_class.setUp()

        funcs = dir(test_class)
        test_queue = TestQueue()

        try:
            for func_name in funcs:
                func = getattr(test_class, func_name)
                if func_name.startswith('test_') and asyncio.iscoroutinefunction(func):
                    try:
                        await self._run_test(func)
                        test_queue.add_success(func_name)
                    except TestFailedException as e:
                        test_queue.add_error(func_name, e)
                    except Exception as e:
                        self.test_logger.log_test_function_exception(func_name, e)
        finally:
            await self._clean_up()

        self.test_logger.log_test_function_results(test_queue)
        return test_queue

    async def _run_module_test_classes(self, module_name: str) -> Dict[str, TestQueue]:
        """Runs all the module test classes"""
        test_queues = {}
        for test_class in self._get_module_classes_by_base_class(module_name, TestCase):
            test_queue = await self._run_class_tests(test_class)
            test_queues[test_class.__name__] = test_queue
            self.test_logger.log_class_results(test_class.__name__, test_queue)

        return test_queues

    async def _run_all_tests(self, loop):
        """Runs all the tests"""
        try:
            for app in self.config.INSTALLED_APPS:
                try:
                    test_results = await self._run_module_test_classes(app + '.test')
                    self.test_logger.log_module_results(app, test_results)
                except Exception as e:
                    self.test_logger.log_module_exception(app, e)
        finally:
            # Clean up
            await self._clean_up()
            self.app.stop()

    async def _clean_up(self):
        """Cleans up the database after testing"""
        for module in self.config.INSTALLED_APPS:
            classes = self._get_module_classes_by_base_class(f'{module}.models', Model)
            for cls in classes:
                if cls.__name__ not in (BaseModel.__name__, Model.__name__):
                    try:
                        await cls.all().delete()
                    except ConfigurationError as e:
                        raise e

    async def _on_run_tests_event(self, app: Sanic, loop: AbstractEventLoop):
        loop.create_task(self._run_all_tests(loop))

    def setup_config(self, config, host, port):
        """Sets up the configuration settings"""
        self.config = config
        self.config.TESTING = True
        self.config.DB_NAME = 'test_' + self.config.DB_NAME
        self.config.HOST = host
        self.config.PORT = port
        self.config.app_events['after_server_start'].append(self._on_run_tests_event)

    def run(self, config, args):
        """Runs the Tester which tests the application <app>
         with <config> and <args>"""
        from application import create_app, run_app
        self.setup_config(
            config=config,
            host=args.H or "localhost",
            port=args.p or 8000
        )
        self.app = create_app(self.config)
        run_app(self.app, access_log=False)


