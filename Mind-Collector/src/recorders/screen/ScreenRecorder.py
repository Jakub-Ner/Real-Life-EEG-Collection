import cv2
import os
import pyautogui
import numpy as np
from multiprocessing import Process, Queue

from src.utils.logger import get_logger
from .config_helpers import ScreenConfig

logger = get_logger(__name__)


class ScreenRecorder(Process):
    """
    User Screen is recorded throughout the whole session.
    """

    def __init__(self, config: ScreenConfig, jobs: Queue):
        super().__init__()
        self.config = config
        self.path = os.path.join(self.config.DATA_PATH, self.config.FILENAME)

    def run(self):
        os.makedirs(self.config.DATA_PATH, exist_ok=True)
        #
        fourcc = cv2.VideoWriter_fourcc(*"XVID")  # type: ignore

        out = cv2.VideoWriter(
            self.path, fourcc, self.config.FPS, self.config.RESOLUTION
        )
        try:
            while True:
                try:
                    ss = np.array(pyautogui.screenshot())
                except OSError as e:
                    logger.error(f"Screen recorder failed to capture screen\n{e}")
                    continue

                ss = cv2.cvtColor(ss, cv2.COLOR_BGR2RGB)
                ss = cv2.resize(ss, self.config.RESOLUTION)
                out.write(ss)

        except KeyboardInterrupt:
            out.release()
            logger.info("Screen recorder has stopped")
