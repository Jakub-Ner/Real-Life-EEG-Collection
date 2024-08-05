import cv2
import os
import time
from tkinter import messagebox
from multiprocessing import Process, Queue

from src.utils.logger import get_logger
from .config_helpers import CameraConfig

logger = get_logger(__name__)


class CameraTriggeredRecorder(Process):
    """
    If many markers are detected in a short (<= DURATION) period of time, the camera recorder will
    record a video only for the first one. The others will be discarded from the queue.
    """

    def __init__(self, config: CameraConfig, jobs: Queue):
        super().__init__()
        self.config = config
        self.jobs = jobs
        self.frames_count = 0
        self.tmp_filename = os.path.join(self.config.DATA_PATH, "tmp.avi")

    def clear_queue(self):
        while not self.jobs.empty():
            self.jobs.get()

    def run(self):
        os.makedirs(self.config.DATA_PATH, exist_ok=True)

        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            messagebox.showerror("Error", "Could not open camera")
            raise SystemExit

        fourcc = cv2.VideoWriter_fourcc(*"XVID")  # type: ignore

        try:
            while True:
                out = cv2.VideoWriter(
                    self.tmp_filename, fourcc, self.config.FPS, self.config.RESOLUTION
                )
                marker = self.jobs.get()

                start = time.time()
                while time.time() - start < self.config.DURATION:
                    ret, frame = camera.read()
                    if not ret:
                        continue
                    out.write(frame)

                self.clear_queue()
                out.release()
                self.frames_count += 1
                frame_path = os.path.join(
                    self.config.DATA_PATH,
                    f"{self.config.FILENAME}-{self.frames_count}-{marker}.avi",
                )
                os.rename(self.tmp_filename, frame_path)
        except KeyboardInterrupt:
            os.remove(self.tmp_filename)
            camera.release()
            logger.info("Camera recorder has stopped")
