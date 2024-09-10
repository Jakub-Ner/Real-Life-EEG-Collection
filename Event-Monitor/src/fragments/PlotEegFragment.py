
import tkinter as tk
from typing import Callable
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from threading import Thread
import numpy as np
import time

from src.utils.Buffer import Buffer
from src.utils.config_helpers import Config


class PlotBaseFragment(tk.Canvas):
  def __init__(self, master, CONFIG: Config, row_transform: Callable[[np.ndarray], float], **kwargs):
    super().__init__(master, **kwargs)
    self.CONFIG = CONFIG
    self.row_transform = row_transform
    self.buffer = Buffer(self.CONFIG.EEG_BUFFER_SIZE)

    self.fig = Figure()
    self.ax = self.fig.add_subplot(111)
    self.canvas = FigureCanvasTkAgg(self.fig, self)

    self.run_thread = True
    self.thread = Thread(target=self.update_plot)
    self.thread.start()

  def update_plot(self):
    while self.run_thread:
      self.ax.clear()
      self.ax.plot(self.buffer.get())
      time.sleep(0.1) # TODO: add to config

  def consume(self, row: np.ndarray):
    # TODO: transform columns by selecting and aggregating|predicting them
    self.buffer.add(row)

  def pack(self, *args, **kwargs):
    self.canvas.draw()
    self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    super().pack(*args, **kwargs)

  def destroy(self):
    self.run_thread = False
    self.thread.join()
    super().destroy()