
import cv2
import os
import time
from tkinter import messagebox
from multiprocessing import Process, Queue

from .config_helpers import CameraConfig

from ..common import get_marker


class CameraRecorder(Process):
    def __init__(self, config: CameraConfig, jobs: Queue):
        super().__init__()
        self.config = config
        self.jobs = jobs
        self.frames_count = 0

    def run(self):
        os.makedirs(self.config.DATA_PATH, exist_ok=True)

        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            messagebox.showerror("Error", "Could not open camera")
            raise SystemExit
        
        while True:
            
            marker = self.jobs.get()
            ret, frame = camera.read()
            if not ret:
                continue

            frame_path = os.path.join(self.config.DATA_PATH, f"{self.frames_count}-{marker}.jpg")
            cv2.imwrite(frame_path, frame)

            time.sleep(self.config.DELAY)
            self.frames_count += 1
