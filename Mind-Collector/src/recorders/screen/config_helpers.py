from dataclasses import dataclass


@dataclass
class ScreenConfig:
    DATA_PATH: str
    FILENAME: str
    DURATION: float = 3.0
    RESOLUTION: tuple[int, int] = (1920, 1080)
    FPS: int = 16
