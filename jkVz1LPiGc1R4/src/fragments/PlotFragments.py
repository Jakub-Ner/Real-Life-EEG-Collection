from threading import Thread
import tkinter as tk
import time
from typing import Generator
import numpy as np

from .PlotEegFragment import PlotEegFragment
from .PlotPredictionsFragment import PlotPredictionsFragment
from src.utils.config_helpers import Config


class PlotFragments(tk.Frame):
  def __init__(self, master, CONFIG: Config, **kwargs):
    super().__init__(master, **kwargs)
    self.CONFIG = CONFIG

    self.left = PlotEegFragment(self, CONFIG)
    self.right = PlotPredictionsFragment(self, CONFIG)

    self.producing_thread = Thread(target=self.produce)
    self.run_thread = True
    self.producing_thread.start()

    
  def pack(self, *args, **kwargs):
    self.left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    self.right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    super().pack(*args, **kwargs)
  
  def produce(self):
    for line in self.read_data():
      if line is None:
        return
      array = np.array(line.split(',')).astype(np.float64)
      self.left.consume(array)
      self.right.consume(array)

  def read_data(self) -> Generator[str|None]:
    self.file = open(self.CONFIG.EEG_PATH, 'r')
    self.file.seek(0, 2) # Seek to the end of the file
    while self.run_thread:
      line = self.file.readline()
      if not line:
        time.sleep(0.1)
        continue
      yield line
    return None

  def destroy(self):
    self.run_thread = False
    self.producing_thread.join()
    self.file.close()
    self.left.destroy()
    self.right.destroy()
    super().destroy()