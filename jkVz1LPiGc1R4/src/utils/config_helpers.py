from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

@dataclass
class EegChannel:
    name: str
    columns: slice
    display: bool = True


@dataclass
class Config:
    TITLE: str = "Event Monitor"
    FRAMES_DELAY: int = 40

    EEG_PATH: str = None
    EEG_CHANNELS: list[EegChannel] = None
    EEG_AGGREGATION: Literal["mean", "max", "min"] = "mean"

    PREDICION_MODEL = 'model.onnx'


