import os
import time
import tkinter as tk
from threading import Thread
from typing import Generator

import numpy as np
from src.utils.config_helpers import Config
from src.utils.logger import get_logger, logging

from .PlotEegFragment import PlotBaseFragment

logger = get_logger(__name__, logging.DEBUG)


class PlotFragments(tk.Canvas):
    def __init__(self, master, CONFIG: Config, **kwargs):
        super().__init__(master, **kwargs)
        self.CONFIG = CONFIG

        self.top_fragment = PlotBaseFragment(
            self,
            self.CONFIG,
            CONFIG.DATA_FRAGMENT.PLOT_FUNCTION,
            CONFIG.DATA_FRAGMENT.ARGUMENTS,
            CONFIG.DATA_FRAGMENT.EEG_YTICKS,
        )
        self.bottom_fragment = PlotBaseFragment(
            self,
            self.CONFIG,
            self.CONFIG.PREDICT_FRAGMENT.PLOT_FUNCTION,
            self.CONFIG.PREDICT_FRAGMENT.ARGUMENTS,
            self.CONFIG.PREDICT_FRAGMENT.EEG_YTICKS,
        )

        self.run_thread = True
        self.thread = Thread(target=self.produce)
        self.thread.start()

    def wait_and_open(self):
        if self.CONFIG.EEG_REALTIME:
            while not os.path.exists(self.CONFIG.EEG_DATA_PATH):
                logger.info(f"Waiting for {self.CONFIG.EEG_DATA_PATH}")
                time.sleep(1)

        self.file = open(self.CONFIG.EEG_DATA_PATH, "r")
        if self.CONFIG.EEG_REALTIME:
            self.file.seek(0, os.SEEK_END) 

    def read_eeg(self) -> Generator[str, None, None]:
        self.wait_and_open()
        while self.run_thread:
            line = self.file.readline()
            if not line:
                time.sleep(self.CONFIG.REFRESH_DELAY / 2)
                continue
            yield line
        return None

    def produce(self, *args, **kwargs):
        for data_row in self.read_eeg():
            logger.debug("Get new row!")
            array = np.fromstring(data_row, sep=self.CONFIG.EEG_DATA_DELIMETER)
            if array.shape[0] > 0:
                logger.debug(array.shape)
                self.top_fragment.consume(array)
                self.bottom_fragment.consume(array)

    def pack(self, *args, **kwargs):
        self.top_fragment.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.bottom_fragment.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        super().pack(*args, **kwargs)

    def destroy(self):
        self.run_thread = False
        self.file.close()
        self.thread.join()

        self.top_fragment.destroy()
        self.bottom_fragment.destroy()

        super().destroy()
