from dataclasses import dataclass


@dataclass
class ScreenshotMarkerConfig:
    """
    Config for the Screenshot Triggered Markers

    Attributes:
    top: tuple[int, int] - top left corner of the marker
    bottom: tuple[int, int] - bottom right corner of the marker
    marker: str - event name
    delay_s: int - delay between consecutive
    """

    TOP: tuple[int, int]
    BOTTOM: tuple[int, int]
    MARKER: str
    EVENT_NAME: str
    DATA_PATH: str
    SAVE_SS: bool = True
    DELAY_S: float = 0.1
