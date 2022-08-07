from typing import List
from .test_queue import TestQueue

import colorama
colorama.init()


class TestLogger:
    def log_module_results(self, app_name: str, test_queues: List[TestQueue]):
        errors = []
        for test_queue in test_queues:
            test_queue_errors = test_queue.get_errors()
            if test_queue_errors:
                errors.append(*test_queue_errors)

        print((colorama.Fore.GREEN if len(errors) == 0 else colorama.Fore.RED) +
              f"All '{app_name}' tests are completed with {len(errors)} errors\n" +
              "-" * 20 + colorama.Fore.RESET)

    def log_module_exception(self, app_name: str, exception: Exception):
        print(colorama.Fore.RED + f"An error occurred during trying to run {app_name} tests: {exception}")

    def log_class_results(self, class_name: str, test_queue: TestQueue):
        errors = test_queue.get_errors()
        print((colorama.Fore.GREEN if len(errors) == 0 else colorama.Fore.RED) +
              f'\tAll {class_name} tests are completed with {len(errors)} errors' +
              colorama.Fore.RESET)

    def log_test_function_results(self, test_queue: TestQueue):
        errors = test_queue.get_errors()
        if len(errors) == 0:
            pass
        else:
            for error in errors:
                print(colorama.Fore.RED + f"\t\tTest {error.name} failed with error: \n{'=' * 20} {error.error} \n{'=' * 20}\n" +
                      colorama.Fore.RESET)

    def log_test_function_exception(self, func_name: str, exception: Exception):
        print(colorama.Fore.RED + f"\t\tAn error: '{exception}' occured in {func_name} test" + colorama.Fore.RESET)

    def log_test_function_done_great(self, func_name: str):
        print(colorama.Fore.GREEN + f"\t\tTest {func_name} completed" + colorama.Fore.RESET)



