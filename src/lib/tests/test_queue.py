from dataclasses import dataclass

from .test import TestFailedException


@dataclass
class TestError:
    name: str
    error: TestFailedException


class TestQueue:
    def __init__(self):
        self.errors_queue = []

    def add_error(self, name: str, error: TestFailedException):
        self.errors_queue.append(TestError(name, error))

    def get_errors(self):
        return self.errors_queue
