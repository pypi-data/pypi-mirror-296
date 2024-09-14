import os
import subprocess
import sys
import time

yellow = "\033[33m"
blue = "\033[34m"
green = "\033[32m"
purple = "\033[35m"
red = "\033[31m"
black = "\033[0m"


def get_terminal_cols():
    return get_windows_cols() if sys.platform.startswith('win') else get_unix_cols()


def get_unix_cols():
    try:
        return ('COLUMNS' in os.environ and int(os.environ['COLUMNS'])) or (
                not os.system('stty size > /dev/null 2>&1') and int(
            subprocess.getstatusoutput('stty size')[1].split()[1]))
    except (ValueError, TypeError, IndexError):
        return None


def get_windows_cols():
    try:
        return int(subprocess.getstatusoutput('mode')[1].split('\n')[4].split(':')[1])
    except (ValueError, TypeError, IndexError):
        return None


def clear_line(cols=get_terminal_cols()):
    print('\r' + (' ' * cols) + '\r', end="")


class ProgressBar:
    def __init__(self, minimum, maximum, supress_exc=False):
        self.min = minimum
        self.max = maximum
        self.value = minimum
        self.message = ""
        self.supress_exc = supress_exc

        self.first_start = None
        self.last_start = None
        self.failed_iterations = 0
        self.iterations = 0

    def iterbegin(self, message: str = None) -> 'ProgressBar':
        if message is not None:
            self.message = message
        if self.first_start is None:
            self.first_start = time.time()
        self.last_start = time.time()
        self.iterations += 1
        return self

    def set_message(self, message: str) -> 'ProgressBar':
        self.message = message
        return self

    def update(self, value) -> 'ProgressBar':
        self.value = value
        return self

    def increment(self, delta=1) -> 'ProgressBar':
        self.value += delta
        return self

    def __str__(self) -> str:
        percentage = self.get_percent()
        fail_percent = self.get_failed_percent()

        return f'[{yellow}{self.message}{black}]:\tCompleted {blue}{percentage}%{black}\t{green}{self.value} / {self.max}{black} failed: {red}{self.failed_iterations} ({fail_percent})%{black}\t{purple}[{self.calc_iter_time()}s / iter]{black}'

    def get_failed_percent(self):
        if self.iterations == 0:
            return float('inf')
        fail_percent = int(100 * self.failed_iterations / self.iterations)
        return fail_percent

    def get_percent(self):
        if self.max == 0:
            return 100
        percentage = int(100 * self.value / self.max)
        return percentage

    def calc_iter_time(self):
        if self.iterations == 0:
            return float('inf')
        return round((time.time() - self.first_start) / self.iterations, 2)

    def print(self) -> 'ProgressBar':
        s = str(self)
        print('\r' + (' ' * len(s)) + ('\b' * len(s)), end="")
        print(' ' + s + "\r", end="")
        return self

    def done(self, message: str = None) -> 'ProgressBar':
        message = message if message is not None else (self.message if self.message is not None else '')
        msg = f'{yellow}[{message}]: {black}Completed {green}{self.value}{black} items ({blue}{self.get_percent()}%{black}); Failed {red}{self.failed_iterations}{black} items {red}({self.get_failed_percent()}%){black}. Average {purple}{self.calc_iter_time()}s / iter{black}'
        clear_line()
        print('\r' + (' ' * len(msg)) + ('\b' * len(msg)), end="")
        print(msg)
        return self

    def iterdone(self):
        self.increment()
        self.print()

    def iterfail(self):
        clear_line()
        print(f'{red}Failed on iteration {self.iterations} {yellow}({self.message}){black}')
        self.failed_iterations += 1

    def __enter__(self):
        self.iterbegin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None and not self.supress_exc:
            raise exc_type(exc_val)
        elif exc_type is not None and self.supress_exc:
            self.iterfail()
            return True
        else:
            self.iterdone()
