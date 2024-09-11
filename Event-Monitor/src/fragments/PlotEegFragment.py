
import tkinter as tk
from typing import Callable
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from threading import Thread
import numpy as np
import time

from src.utils.Buffer import Buffer
from src.utils.config_helpers import Config
from src.utils.logger import get_logger

logger = get_logger(__name__)

class PlotBaseFragment(tk.Canvas):
  def __init__(self, master, CONFIG: Config, row_transform: Callable[[np.ndarray], float], **kwargs):
    super().__init__(master, **kwargs)
    self.CONFIG = CONFIG
    self.row_transform = row_transform
    self.buffer = Buffer(shape=(CONFIG.EEG_BUFFER_SIZE, len(CONFIG.EEG_CHANNELS) + 1))

    self.fig = Figure()
    self.ax = self.fig.add_subplot(111)

    X_LABELS = ["t-3", "t-2", "t-1", "t"] # TODO: regard sampling rate
    self.ax.set_xticks(range(4))
    self.ax.set_xticklabels(X_LABELS)
    self.ax.set_xlabel("Time")
    self.ax.set_ylabel(self.row_transform.__name__)
    Y_LABELS = range(0, 20, 4)  # TODO: add to config
    self.ax.set_yticks(Y_LABELS)
    self.ax.set_yticklabels(Y_LABELS)

    self.plota = Line2D([], [])
    self.plota.set_label("alpha")
    self.plota.set_color('blue')
    self.ax.add_line(self.plota)

    self.plotb = Line2D([], [])
    self.plotb.set_label("beta")
    self.plotb.set_color('red')
    self.ax.add_line(self.plotb)


    self.canvas = FigureCanvasTkAgg(self.fig, self)

    self.run_thread = True
    self.thread = Thread(target=self.update_plot)
    self.thread.start()

  def plot_markers(self, marker: int):...
      # TODO
      # self.ax.axvline(x=marker, color='r') # TODO: use diff colors

  def update_plot(self):
    while self.run_thread:
      data = self.buffer.get()
      self.plota.set_data(range(len(self.buffer)), data[:, 0])
      self.plotb.set_data(range(len(self.buffer)), data[:, 1])
      self.plot_markers(int(data[:, -1]))
      self.ax.legend()
      time.sleep(0.1) # TODO: add to config

  def consume(self, row: np.ndarray):
    aggregated_row = np.array(
      [self.row_transform(row[channel.columns]) for channel in self.CONFIG.EEG_CHANNELS] + [row[-1]]
    )
    self.buffer.add(aggregated_row)

  def pack(self, *args, **kwargs):
    self.canvas.draw()
    self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    super().pack(*args, **kwargs)

  def destroy(self):
    self.run_thread = False
    self.thread.join()
    super().destroy()