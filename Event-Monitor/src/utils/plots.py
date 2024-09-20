from typing import Iterable
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.colors import TABLEAU_COLORS, XKCD_COLORS # type: ignore
import matplotlib.pyplot as plt


from src.utils.config_helpers import Config, PlotArgument

def calculate_xticks(frequency: int, size: int, labels_num: int = 4) -> dict[str,Iterable]:
  diff = size // (frequency * labels_num)
  labels = [f'-{i*diff}s' for i in range(labels_num-1, 0, -1)] + ['Now']
  ticks = range(diff * frequency, size+1, diff * frequency)
  return {'labels': labels, 'ticks': ticks}


def get_colors(number_of_colors):
  if number_of_colors > len(TABLEAU_COLORS):
        return iter(XKCD_COLORS.values())
  else:
      return iter(TABLEAU_COLORS.values()) 


def prepare_figure(CONFIG: Config, ylabel: str, yticks: Iterable) -> tuple[Figure, plt.Axes]:
  fig = Figure()
  ax = fig.add_subplot(111)
  ax.set_xlim(0, CONFIG.EEG_BUFFER_SIZE)
  ax.set_xlabel("Time")
  ax.set_xticks(**calculate_xticks(CONFIG.EEG_SAMPLING_RATE, CONFIG.EEG_BUFFER_SIZE, CONFIG.EEG_XTICKS))
  ax.set_ylabel(ylabel)
  ax.set_yticks(yticks)

  # add labels for markers
  colors = get_colors(len(CONFIG.MARKERS)) 
  x_margin, y_margin = 10, 10
  for i, key in enumerate(CONFIG.MARKERS):
    ax.annotate(f"--- {CONFIG.MARKERS[key]}", xy=(x_margin, (i+1)*y_margin), color=next(colors), xycoords='axes points', size=y_margin)
  return fig, ax

def prepare_lines(channels: list[PlotArgument]) -> list[Line2D]:
  colors = get_colors(len(channels))
  lines = []
  for channel in channels:
    line = Line2D([], [], color=next(colors), label=channel.name)
    # TODO: if not display, set line to invisible
    lines.append(line)
  return lines 

