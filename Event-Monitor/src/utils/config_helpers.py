from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Iterable
import numpy as np

@dataclass
class PlotArgument:
    name: str
    columns: slice
    display: bool = True

@dataclass
class PlotFragmentConfig:
    PLOT_FUNCTION: Callable[[np.ndarray], np.ndarray]
    EEG_YTICKS: Iterable[float|int]
    ARGUMENTS: list[PlotArgument]

@dataclass
class Config:
    EEG_SAMPLING_RATE: int
    EEG_DATA_PATH: str
    EEG_CHANNELS: list[PlotArgument]

    DATA_FRAGMENT: PlotFragmentConfig
    PREDICT_FRAGMENT: PlotFragmentConfig

    MARKERS: dict[str, str]

    TITLE: str = "Event Monitor"
    REFRESH_DELAY: float = 0.04 # seconds

    EEG_BUFFER_SIZE: int = 100
    EEG_REALTIME: bool = False
 
    EEG_XTICKS: int = 4

 

