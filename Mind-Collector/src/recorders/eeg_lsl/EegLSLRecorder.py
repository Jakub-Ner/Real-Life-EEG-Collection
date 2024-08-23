from __future__ import annotations

import time
from multiprocessing import Process, Queue
import os
import numpy as np
from queue import Empty
from tkinter import messagebox
import logging
import json

from pylsl import resolve_stream, StreamInlet, pylsl

from src.utils.logger import get_logger
from .config_helpers import FORMAT, EegLslConfig

logger = get_logger(__name__, logging.INFO)

from typing import TypedDict, List

class ToSave(TypedDict):
    data: List[any]   
    marker: str

class EegLSLRecorder(Process):
    previous_ts = 0

    def __init__(self, config: EegLslConfig, jobs: Queue):
        super().__init__()
        self.config = config
        self.jobs = jobs

    def turn_off(self):
        logger.info("Turning off LSLStreamer")

    def parse_message(self, to_save: ToSave) -> str | bytearray:
        if self.config.OUTPUT_FORMAT == FORMAT.ASCII:
            try:
                return json.dumps(to_save) + '\n'
            except UnicodeDecodeError:
                logger.error("Error decoding message")
                return ""
        else:
            return json.dumps(to_save).encode('utf-8') + b'\n'

    def run(self):
        os.makedirs(self.config.DATA_PATH, exist_ok=True)
        self.record(os.path.join(self.config.DATA_PATH, self.config.FILENAME))

    def record(self, path: str):
        file_mode = "w+" if self.config.OUTPUT_FORMAT == FORMAT.ASCII else "wb+"
        self.file = open(path, file_mode)
        logger.debug("Saving to " + path)

        logger.info("Looking for an LSL stream ...")
        streams = []
        while not streams:
            streams = resolve_stream('name', self.config.STREAM_NAME)
            time.sleep(1)
        logger.info("LSL stream found: {}".format(streams[0].name()))
        inlet = StreamInlet(streams[0], pylsl.proc_threadsafe)
        try:
            while True:
                data_chunk, timestamp = inlet.pull_chunk(timeout=self.config.PULL_TIMEOUT)
                timestamp = pylsl.local_clock()
                delta_ts = np.round(timestamp - self.previous_ts, 2) if self.previous_ts != 0 else 0
                self.previous_ts = timestamp
                logger.debug(f"New sample: {data_chunk} after {delta_ts}")
                if data_chunk:
                    try:
                        marker = self.jobs.get_nowait()
                    except Empty:
                        marker = "0"

                    to_save = {
                        'data': data_chunk,
                        'marker': marker,
                    }
                    if msg := self.parse_message(to_save):
                        logger.debug(f"<msg>{msg}</msg>")
                        self.file.write(msg)

        except Exception as ex:
            messagebox.showerror("Error", f"Error during UDP data acquisition:\n{ex}")
        finally:
            logger.info("LSLStreamer finally closed")
            self.file.close()
