from multiprocessing import Queue
import os
import warnings

from .utils.helpers import Streamer, Recorder
from .configuration import CONFIG

warnings.filterwarnings("ignore")


class EEGRecorder(Recorder):
    def __init__(self, name_prefix: str, jobs: Queue) -> None:
        super().__init__(jobs)
        self.filename = name_prefix
        self.streamer: Streamer = CONFIG.streamer.CLASS(**CONFIG.streamer.__dict__)

    def run(self):
        if not os.path.exists(CONFIG.EEG_PATH):
            os.mkdir(CONFIG.EEG_PATH)


        try:
            path = os.path.join(CONFIG.EEG_PATH, self.filename)
            self.streamer.record(path, self.jobs)
        except KeyboardInterrupt:...

    def terminate(self) -> None:
        self.streamer.turn_off()
        return super().terminate()