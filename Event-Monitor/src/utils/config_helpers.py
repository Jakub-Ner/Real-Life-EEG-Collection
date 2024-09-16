from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Literal
import numpy as np

@dataclass
class EegChannel:
    name: str
    columns: slice
    display: bool = True
    
@dataclass
class Config:
    EEG_SAMPLING_RATE: int
    EEG_DATA_PATH: str
    EEG_CHANNELS: list[EegChannel]
    EEG_AGGREGATION: Callable[[np.ndarray], np.ndarray] # don't use lambdas, because plot calls Callable.__name__ 
    EEG_MARKERS: dict[str, str]

    TITLE: str = "Event Monitor"
    REFRESH_DELAY: float = 0.04 # seconds

    EEG_BUFFER_SIZE: int = 100
    EEG_REALTIME: bool = False
    EEG_XTICKS: int = 4
    EEG_YTICKS: range = range(10, 20, 4)
 
    EEG_PREDICTION: Callable[[np.ndarray], np.ndarray]|None = None

