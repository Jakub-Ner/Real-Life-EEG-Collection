from multiprocessing import Process, Queue
import random
from ahk import AHK
import time
from pynput import keyboard
import logging

from src.utils.common import parse_duration
from src.utils.logger import get_logger
from .config_helpers import RandomClickConfig

logger = get_logger(__name__, logging.ERROR)


class RandomClick(Process):
    def __init__(
        self,
        config: RandomClickConfig,
        recorder_jobs: Queue,
    ) -> None:
        super().__init__()

        self.config = config
        self.time_to_wait = 0
        self.starting_time = time.time()
        self.is_triggered = False
        self.recorder_jobs = recorder_jobs

        self.init_key_listener()

    def run(self):
        self.ahk = AHK()  # can't be in __init__ because it's a different process

        try:
            while True:
                self.wait()
                self.recorder_jobs.put(self.config.KEY)
                self.trigger()
        except KeyboardInterrupt:
            logger.info(f"Random click has stopped")

    def init_key_listener(self):
        key_listener = keyboard.Listener(on_press=self.on_press)
        key_listener.daemon = True
        key_listener.start()

    def set_timer(self):
        self.time_to_wait = random.choice(self.config.RANDOM_RANGE)

    def on_press(self, key):
        if self.is_triggered:
            self.is_triggered = False
            return
        if self.config.KEY == str(key).strip("'"):
            logger.info(f"User pressed {self.config.KEY}, timer will reset.")
            self.set_timer()

    def wait(self):
        self.set_timer()

        while self.time_to_wait > 0:
            time.sleep(1)
            self.time_to_wait -= 1

    def trigger(self):
        self.is_triggered = True
        self.ahk.key_down(self.config.KEY)
        time.sleep(0.1)
        self.ahk.key_up(self.config.KEY)

        since_start = time.time() - self.starting_time
        logger.info(f"Triggered event {parse_duration(since_start)} since start")
