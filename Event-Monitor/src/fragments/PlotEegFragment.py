import time
import tkinter as tk
from threading import Thread
from typing import Callable, Iterable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.utils.Buffer import Buffer
from src.utils.config_helpers import Config, PlotArgument
from src.utils.logger import get_logger
from src.utils.plots import prepare_figure, prepare_lines, get_colors

logger = get_logger(__name__)


class PlotBaseFragment(tk.Canvas):
    def __init__(
        self,
        master,
        CONFIG: Config,
        row_transform: Callable[[np.ndarray], np.ndarray],
        arguments: list[PlotArgument],
        yticks: Iterable,
        **kwargs,
    ):
        super().__init__(master, **kwargs)
        self.CONFIG = CONFIG
        self.row_transform = row_transform
        self.arguments = arguments
        self.buffer = Buffer(shape=(CONFIG.EEG_BUFFER_SIZE, len(arguments) + 1))
        self.yticks = yticks

        self.prepare_plt()
        self.marker_colors = list(get_colors(len(CONFIG.MARKERS)))
        self.run_thread = True
        self.thread = Thread(target=self.update_plot)
        self.thread.start()

        self.deb_counter = 0

    def prepare_plt(self):
        plt.style.use("ggplot")  # use plt.style.available to se more
        self.fig, self.ax = prepare_figure(
            self.CONFIG, self.row_transform.__name__, self.yticks
        )
        self.lines = prepare_lines(self.arguments)
        for line in self.lines:
            self.ax.add_line(line)
        self.marker_lines = []
        self.canvas = FigureCanvasTkAgg(self.fig, self)

    def plot_markers(self, markers: np.ndarray):
        lines_to_remove = []
        for i, line in enumerate(self.marker_lines):
            prev_x, prev_y = line.get_data()
            if prev_x[0] == 0:
                lines_to_remove.append(i)
            else:
                line.set_data([prev_x[0] - 1, prev_x[0] - 1], prev_y)
        for i in lines_to_remove:
            self.marker_lines.pop(i).remove()

    def update_plot(self):
        while self.run_thread:
            data = self.buffer.get()
            xs = range(len(self.buffer))

            for i, line in enumerate(self.lines):
                line.set_data(xs, data[:, i])

            self.plot_markers(data[:, -1])
            self.ax.legend(loc="upper left")
            time.sleep(self.CONFIG.REFRESH_DELAY)

    def consume(self, row: np.ndarray):
        self.deb_counter += 1
        aggregated_row = self.row_transform(
            np.array([row[channel.columns] for channel in self.CONFIG.EEG_CHANNELS])
        )
        marker = int(row[-1])
        aggregated_row = np.append(aggregated_row, values=[marker])
        if marker != 0:
            self.marker_lines.append(
                self.ax.axvline(x=len(self.buffer), color=self.marker_colors[marker -11], linestyle="--")
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
