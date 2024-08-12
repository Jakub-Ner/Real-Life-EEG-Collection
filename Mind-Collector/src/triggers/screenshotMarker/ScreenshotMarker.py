from multiprocessing import Process, Queue
import pyautogui
from time import sleep
import numpy as np
import cv2
from src.utils.logger import get_logger
from .config_helpers import ScreenshotMarkerConfig

logger = get_logger(__name__)

EPSILON = 0.01


class ScreenshotMarker(Process):
    def __init__(
        self,
        config: ScreenshotMarkerConfig,
        recorder_jobs: Queue,
    ) -> None:
        super().__init__()
        self.config = config

        self.width = self.config.BOTTOM[0] - self.config.TOP[0]
        self.height = self.config.BOTTOM[1] - self.config.TOP[1]
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
                    self.config.TOP[0],
                    self.config.TOP[1],
                    self.width,
                    self.height,
                )
            )
            .convert("L")
            .point(lambda p: 255 if p > 128 else 0)
        )
        return np.array(ss)

    def run(self):
        try:
            sleep(5)  # wait for the game to start
            logger.info(f"Screenshot Marker has started")
            while True:
                ss = self.take_screenshot()
                if self.ss_changed(ss):
                    self.recorder_jobs.put(self.config.MARKER)
                    if self.config.SAVE_SS:
                        cv2.imwrite(
                            f"{self.config.OUT_PATH}/{self.config.MARKER}_{self.counter}.png",
                            ss,
                        )
                        self.counter += 1

                    logger.info(f"Screenshot marker {self.config.MARKER} triggered")
                sleep(self.config.DELAY_S)
        except KeyboardInterrupt:
            logger.info(f"Screenshot Marker has stopped")
