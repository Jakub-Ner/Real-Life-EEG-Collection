
import tkinter as tk
from typing import Generator
import numpy as np
import time
from threading import Thread

from .PlotEegFragment import PlotBaseFragment
from src.utils.config_helpers import Config


class PlotFragments(tk.Canvas):
  def __init__(self, master, CONFIG: Config, **kwargs):
    super().__init__(master, **kwargs)
    self.CONFIG = CONFIG

    self.left_fragment = PlotBaseFragment(self, self.CONFIG, CONFIG.EEG_AGGREGATION)
    # TODO: check if CONFIG.EEG_PREDICTION is not None
    self.right_fragment = PlotBaseFragment(self, self.CONFIG, self.CONFIG.EEG_PREDICTION) # type: ignore

    self.run_thread = True
    self.thread = Thread(target=self.produce)
    self.thread.start()

  def read_eeg(self) -> Generator[str, None, None]:
    # TODO: validate is not None
    self.file = open(self.CONFIG.EEG_DATA_PATH, 'r')
    if self.CONFIG.EEG_REALTIME:
        self.file.seek(0, 2)
      
    while self.run_thread:
      line = self.file.readline()
      if not line:
        time.sleep(0.1)
        continue
      yield line
    return None

  def produce(self, *args, **kwargs) :
    for data_row in self.read_eeg():
      array = np.fromstring(data_row, sep=',')
      self.left_fragment.consume(array)
      self.right_fragment.consume(array)
    

  def pack(self, *args, **kwargs):
    self.left_fragment.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    self.right_fragment.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    super().pack(*args, **kwargs)

  def destroy(self):
    self.run_thread = False
    self.file.close()
    self.thread.join()

    self.left_fragment.destroy()
    self.right_fragment.destroy()

    super().destroy()


