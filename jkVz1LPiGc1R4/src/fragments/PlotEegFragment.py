
import tkinter as tk

from PIL import ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
from threading import Thread
import time
from src.utils.config_helpers import Config

class PlotEegFragment(tk.Canvas):
  def __init__(self, master, CONFIG: Config, **kwargs):
    super().__init__(master, **kwargs)
    self.CONFIG = CONFIG

    self.buffer: list[np.ndarray] = []

    self.fig, self.ax = plt.subplots(1)
    self.plot = FigureCanvasTkAgg(self.fig, master=self)
    self.plot.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    self.update_thread = Thread(target=self.update_plot)
    self.run_thread = True
    self.update_thread.start()
    
  def consume(self, data: np.ndarray):
    self.buffer.append(data)
    
  def update_plot(self):
    while self.run_thread:
      xs = np.linspace(self.x, 10)
      ys = np.sin(xs * 180 * np.pi)
      self.x += 1

      self.ax.clear()
      self.ax.plot(xs, ys)

      time.sleep(0.5)

  def pack(self, *args, **kwargs):
    self.plot.draw()
    super().pack(*args, **kwargs)

  def destroy(self):
    self.run_thread = False
    self.update_thread.join()
    super().destroy()