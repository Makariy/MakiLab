from typing import List, Union
from dataclasses import dataclass

from .test import TestFailedException


@dataclass
class TestError:
    name: str
    error: TestFailedException


@dataclass
class TestSuccess:
    name: str


class TestQueue:
    def __init__(self):
        self.queue: List[Union[TestError, TestSuccess]] = []

    def add_error(self, name: str, error: TestFailedException):
        self.queue.append(TestError(name, error))

    def add_success(self, name: str):
        self.queue.append(TestSuccess(name))

    def get_errors(self) -> List[TestError]:
        return list(filter(lambda a: type(a) is TestError, self.queue))

    def get_success(self) -> List[TestSuccess]:
        return list(filter(lambda a: type(a) is TestSuccess, self.queue))

    def get_queue(self) -> List[Union[TestSuccess, TestError]]:
        return self.queue

