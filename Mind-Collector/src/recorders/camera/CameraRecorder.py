import cv2
import os
from tkinter import messagebox
from multiprocessing import Process, Queue

from src.utils.logger import get_logger
from .config_helpers import CameraConfig

logger = get_logger(__name__)


class CameraRecorder(Process):
    """
    Camera is recording throughout the whole session.
    """

    def __init__(self, config: CameraConfig, jobs: Queue):
        super().__init__()
        self.config = config
        self.path = os.path.join(self.config.DATA_PATH, self.config.FILENAME)

    def run(self):
        os.makedirs(self.config.DATA_PATH, exist_ok=True)

        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            messagebox.showerror("Error", "Could not open camera")
            raise SystemExit

        fourcc = cv2.VideoWriter_fourcc(*"XVID")  # type: ignore

        try:
            out = cv2.VideoWriter(
                self.path, fourcc, self.config.FPS, self.config.RESOLUTION
            )

            while True:
                ret, frame = camera.read()
                if not ret:
                    continue
                out.write(frame)

        except KeyboardInterrupt:
            camera.release()
            logger.info("Camera recorder has stopped")
