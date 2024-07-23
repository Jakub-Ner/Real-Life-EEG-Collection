from dataclasses import dataclass


@dataclass
class ScreenshotMarkerConfigType:
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
    DELAY_S: float = 0.1
