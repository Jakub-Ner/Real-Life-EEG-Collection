import time


def get_now(as_path=False):
    if as_path:
        return time.strftime("%Y-%m-%dT%H-%M-%S")
    return time.strftime("%Y-%m-%d %H:%M:%S")


def parse_duration(duration: int | float):
    duration_minutes = duration // 60
    duration_seconds = duration % 60
    return f"{duration_minutes}:{int(duration_seconds)}"
