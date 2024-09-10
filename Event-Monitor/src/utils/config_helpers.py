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
    TITLE: str = "Event Monitor"
    REFRESH_DELAY: int = 300

    EEG_DATA_PATH: str = "./eeg_data.csv"
    EEG_BUFFER_SIZE: int = 100
    EEG_REALTIME: bool = False
    EEG_CHANNELS: list[EegChannel]|None = None
    EEG_AGGREGATION: Callable[[np.ndarray], float] = lambda row: row.mean(axis=0)
    EEG_MARKERS: dict[str, str] = {'0': 'none', '1': 'kill', '2': 'death'}

    # TODO: EEG_PREDICTION
    EEG_PREDICTION: Callable[[np.ndarray], float] = lambda row: row.mean(axis=0) # TODO: replace with model.predict

