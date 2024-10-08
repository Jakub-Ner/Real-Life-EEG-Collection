from dataclasses import dataclass


@dataclass
class CameraConfig:
    DATA_PATH: str
    FILENAME: str
    RESOLUTION: tuple[int, int] = (640, 480)
    DURATION: float = 3.0
    FPS: int = 20
