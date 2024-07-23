
from multiprocessing import Queue
from queue import Empty


def get_marker(jobs: Queue, default: str = "0") -> str:
    try:
        return jobs.get(block=False)
    except Empty:
        return default