import time
import os
from uuid import uuid4

from utils.listen_udp import listen_udp

def get_now():
    return time.strftime("%Y-%m-%d %H:%M:%S")

def parse_duration(duration: int):
    duration_minutes = duration // 60
    duration_seconds = duration % 60
    return f"{duration_minutes}:{int(duration_seconds)}"

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

def assert_udp(func, *args, **kwargs):
    def decorated_func(*args, **kwargs):
        try:
            listen_udp('test', 0.1, dialogue_box=False)
        except Exception as ex:
            raise Exception("UDP data acquisition failed, Make sure the UDP server is running.")
        finally:
            os.remove(f'test.csv')
        return func(*args, **kwargs)
    return decorated_func

class EEGEvent:
    def __init__(self, state_duration) -> None:
        self.state_duration = state_duration

    def wait(self):...
    def trigger(self):...
