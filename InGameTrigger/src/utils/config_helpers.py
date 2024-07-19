from dataclasses import dataclass, field

from .common import get_now
from .logger import get_logger

logger = get_logger(__name__)


@dataclass
class GeneralConfig:
    FILENAME_PREFIX: str

    def __post_init__(self):
        self.FILENAME_PREFIX = f"{self.FILENAME_PREFIX}_{get_now(True)}"


@dataclass
class RandomClickConfig:
    KEY: str
    STATE_DURATION: int  # in seconds
    RANDOM_RANGE: tuple[int, int, int]  # (start, stop, step)


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
    DELAY_S: float = 0.1


@dataclass
class Config:
    general: GeneralConfig
    randomClick: RandomClickConfig | None = None
    ssMarkers: list[ScreenshotMarkerConfig] = field(default_factory=list)

    def __post_init__(self):
        logger.info(self)

    def __repr__(self) -> str:
        return f"""
Active configuration: {{
    general: {self.general},
    randomClick: {self.randomClick},
    ScreenshotMarkerConfig: [
{chr(10).join(f'        {marker},' for marker in self.ssMarkers)}
    ]
}}"""
