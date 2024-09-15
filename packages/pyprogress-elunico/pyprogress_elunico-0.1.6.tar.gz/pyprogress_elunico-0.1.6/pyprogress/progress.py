import shutil
import time

black = "\033[0m"
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
purple = "\033[35m"

def get_terminal_cols():
    return shutil.get_terminal_size().columns

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

    def iterdone(self):
        self.increment()
        self.print()

    def iterfail(self):
        clear_line()
        print(f'{red}Failed on iteration {self.iterations} {yellow}({self.message}){black}')
        self.failed_iterations += 1

    def set_message(self, message: str) -> 'ProgressBar':
        self.message = message
        return self

    def update(self, value) -> 'ProgressBar':
        self.value = value
        return self

    def increment(self, delta=1) -> 'ProgressBar':
        self.value += delta
        return self

    def get_failed_percent(self):
        if self.iterations == 0:
            return float('inf')
        fail_percent = int(100 * self.failed_iterations / self.max)
        return fail_percent

    def get_percent(self):
        if self.max == 0:
            return 100
        percentage = int(100 * self.iterations / self.max)
        return percentage

    def calc_iter_time(self):
        if self.iterations == 0:
            return float('inf')
        return round((time.time() - self.first_start) / self.iterations, 2)

    def print(self) -> 'ProgressBar':
        clear_line()
        print(' ' + str(self) + "\r", end="")
        return self

    def done(self, message: str = None) -> 'ProgressBar':
        message = message if message is not None else (self.message if self.message is not None else '')
        msg = f'{yellow}[{message}]: {black}Completed {green}{self.value}{black} items ({blue}{self.get_percent()}%{black}); Failed {red}{self.failed_iterations}{black} items {red}({self.get_failed_percent()}%){black}. Average {purple}{self.calc_iter_time()}s / iter{black}'
        clear_line()
        print(msg)
        return self

    def __str__(self) -> str:
        percentage = self.get_percent()
        fail_percent = self.get_failed_percent()

        return f'[{yellow}{self.message}{black}]:\tCompleted {blue}{percentage}%{black}\t{green}{self.value} / {self.max}{black} failed: {red}{self.failed_iterations} ({fail_percent})%{black}\t{purple}[{self.calc_iter_time()}s / iter]{black}'

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
