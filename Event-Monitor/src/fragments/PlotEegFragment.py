
import tkinter as tk
from typing import Callable
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from threading import Thread
import numpy as np
import time

from src.utils.Buffer import Buffer
from src.utils.config_helpers import Config, EegChannel
from src.utils.logger import get_logger
from src.utils.plots import prepare_figure, prepare_lines

logger = get_logger(__name__)


class PlotBaseFragment(tk.Canvas):
  def __init__(self, master, CONFIG: Config, row_transform: Callable[[np.ndarray], float], **kwargs):
    super().__init__(master, **kwargs)
    self.CONFIG = CONFIG
    self.row_transform = row_transform
    self.buffer = Buffer(shape=(CONFIG.EEG_BUFFER_SIZE, len(CONFIG.EEG_CHANNELS) + 1))

    self.prepare_plt()

    self.run_thread = True
    self.thread = Thread(target=self.update_plot)
    self.thread.start()

    self.deb_counter = 0

  def prepare_plt(self):
    plt.style.use('ggplot') # use plt.style.available to se more
    self.fig, self.ax = prepare_figure(self.CONFIG, self.row_transform.__name__)
    self.lines = prepare_lines(self.CONFIG.EEG_CHANNELS)
    for line in self.lines:
      self.ax.add_line(line)
    
    self.canvas = FigureCanvasTkAgg(self.fig, self)
  
  def plot_markers(self, markers: np.ndarray):...
      # TODO
      # self.ax.axvline(x=marker, color='r') # TODO: use diff colors

  def update_plot(self):
    while self.run_thread:
      data = self.buffer.get()
      xs = range(len(self.buffer))

      for i, line in enumerate(self.lines):
        line.set_data(xs, data[:, i])

      self.plot_markers(data[:, -1])
      self.ax.legend(bbox_to_anchor=(0.01, 0.01), loc='lower left')
      time.sleep(self.CONFIG.REFRESH_DELAY)

  def consume(self, row: np.ndarray):
    self.deb_counter += 1
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