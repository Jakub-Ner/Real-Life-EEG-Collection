from multiprocessing import Queue
import pyautogui
from time import sleep
import numpy as np

from src.utils.common import AbstractTrigger, get_now
from src.utils.logger import get_logger


logger = get_logger(__name__)

EPSILON = 0.01


class ScreenshotMarker(AbstractTrigger):
    def __init__(
        self,
        top: tuple[int, int],
        bottom: tuple[int, int],
        marker: str,
        delay_s: float,
        recorder_jobs: Queue,
    ) -> None:
        super().__init__()
        self.top = top
        self.bottom = bottom
        self.width = self.bottom[0] - self.top[0]
        self.height = self.bottom[1] - self.top[1]
        self.marker = marker
        self.delay_s = delay_s
        self.recorder_jobs = recorder_jobs
        self.previous_ss = None
        self.counter = 0

    def ss_changed(self, ss):
        if self.previous_ss is None:
            self.previous_ss = ss
            return False

        if np.mean((self.previous_ss - ss) ** 2) > EPSILON:
            self.previous_ss = ss
            return True
        return False

    def take_screenshot(self):
        ss = (
            pyautogui.screenshot(
                region=(
                    self.top[0],
                    self.top[1],
                    self.width,
                    self.height,
                )
            )
            .convert("L")
            .point(lambda p: 255 if p > 128 else 0)
        )
        return np.array(ss)

    def run(self):
        # sleep(10) # wait for the game to start
        logger.info(f"Screenshot Marker started at {get_now()}")
        while True:
            ss = self.take_screenshot()
            if self.ss_changed(ss):
                self.recorder_jobs.put(self.marker)
                logger.info(f"Screenshot marker {self.marker} triggered")
            sleep(self.delay_s)
