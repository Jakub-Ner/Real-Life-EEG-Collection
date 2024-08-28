from multiprocessing import Process, Queue
import random
from ahk import AHK
import time
import pyautogui
import numpy as np
from pynput import keyboard
import logging

from src.utils.common import parse_duration
from src.utils.logger import get_logger
from .config_helpers import RandomClickConfig

logger = get_logger(__name__, logging.INFO)


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
                self.recorder_jobs.put(self.config.MARKER)
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
            logger.debug(f"User pressed {self.config.KEY}, timer will reset.")
            self.set_timer()

    def is_player_dead(self):
        if not (self.config.DEATH_AREA_TOP and self.config.DEATH_AREA_BOTTOM):
            return False
        
        top_left = self.config.DEATH_AREA_TOP
        bottom_right = self.config.DEATH_AREA_BOTTOM
        screenshot = pyautogui.screenshot(
            region=(top_left[0], top_left[1], bottom_right[0] - top_left[0], bottom_right[1] - top_left[1])
            )
        arr = np.array(screenshot)
        num_of_non_gray_pixels = len(arr[(arr[:,:,0] != arr[:,:,1]) | (arr[:,:,1] != arr[:,:,2])])
        if num_of_non_gray_pixels < 100:
            return True 
        return False

    def wait(self):
        self.set_timer()

        while self.time_to_wait > 0:
            time.sleep(1)
            self.time_to_wait -= 1
            
        while self.is_player_dead():
            time.sleep(1)
            logger.debug("Player is dead, waiting for respawn")


    def trigger(self):
        self.is_triggered = True
        self.ahk.key_down(self.config.KEY)
        time.sleep(0.1)
        self.ahk.key_up(self.config.KEY)

        since_start = time.time() - self.starting_time
        logger.info(f"Triggered event {parse_duration(since_start)} since start")
