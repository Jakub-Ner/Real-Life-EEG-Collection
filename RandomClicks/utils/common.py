import time
from uuid import uuid4

def get_now():
    return time.strftime("%Y-%m-%d %H:%M:%S")

def parse_range(func, *args, **kwargs):
    def decorated_func(*args, **kwargs):
        kwargs['random_range'] = range(*kwargs['random_range'])
        return func(*args, **kwargs)
    return decorated_func

def parse_filename(func, *args, **kwargs):
    def decorated_func(*args, **kwargs):
        kwargs['filename'] = f'{kwargs["filename"]}-{uuid4().hex[:4]}'
        return func(*args, **kwargs)
    return decorated_func

class EEGEvent:
    def __init__(self, state_duration) -> None:
        self.state_duration = state_duration

    def wait(self):...
    def trigger(self):...
