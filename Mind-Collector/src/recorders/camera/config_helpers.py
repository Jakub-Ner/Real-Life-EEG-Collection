from dataclasses import dataclass


@dataclass
class CameraConfig:
    DATA_PATH: str
    DURATION: float
    FPS: int = 20
