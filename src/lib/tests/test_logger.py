from typing import Dict
from .test_queue import TestQueue

import colorama
colorama.init()


class TestLogger:
    def log_module_results(self, app_name: str, test_results: Dict[str, TestQueue]):
        errors = []
        successes = []
        for results in test_results.values():
            queue_errors = results.get_errors()
            queue_successes = results.get_success()
            if queue_errors:
                errors = [*errors, *queue_errors]
            if queue_successes:
                successes = [*successes, *queue_successes]

        print((colorama.Fore.GREEN if len(errors) == 0 else colorama.Fore.RED) +
              f"All '{app_name}' {len(errors) + len(successes)} tests are completed with {len(errors)} errors\n" +
              "-" * 20 + colorama.Fore.RESET)

    def log_class_results(self, class_name: str, test_queue: TestQueue):
        errors = test_queue.get_errors()
        queue = test_queue.get_queue()
        print((colorama.Fore.GREEN if len(errors) == 0 else colorama.Fore.RED) +
              f"\tAll {class_name}'s {len(queue)} tests are completed with {len(errors)} errors\n" +
              colorama.Fore.RESET)

    def log_test_function_results(self, test_queue: TestQueue):
        errors = test_queue.get_errors()
        successes = test_queue.get_success()
        if successes:
            for success in successes:
                print(colorama.Fore.GREEN + f"\t\tTest {success.name} completed" + colorama.Fore.RESET)

        if errors:
            for error in errors:
                print(colorama.Fore.RED + f"\t\tTest {error.name} failed with error: \n{'=' * 20} {error.error} \n{'=' * 20}\n" +
                      colorama.Fore.RESET)

    def log_module_exception(self, app_name: str, exception: Exception):
        print(colorama.Fore.RED + f"An error occurred during trying to run {app_name} tests: {exception}")

    def log_test_function_exception(self, func_name: str, exception: Exception):
        print(colorama.Fore.RED + f"\t\tAn error: '{exception}' occured in {func_name} test" + colorama.Fore.RESET)


