from dataclasses import dataclass, field

from .common import get_now
from .logger import get_logger

logger = get_logger(__name__)


@dataclass
class GeneralConfigType:
    FILENAME_PREFIX: str

    def __post_init__(self):
        self.FILENAME_PREFIX = f"{self.FILENAME_PREFIX}_{get_now(True)}"


@dataclass
class RandomClickConfigType:
    KEY: str
    STATE_DURATION: int  # in seconds
    RANDOM_RANGE: tuple[int, int, int]  # (start, stop, step)


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


@dataclass
class ConfigType:
    general: GeneralConfigType
    randomClick: RandomClickConfigType | None = None
    ssMarkers: list[ScreenshotMarkerConfigType] = field(default_factory=list)

    # def __post_init__(self):
    #     logger.info(self)

    def __repr__(self) -> str:
        return f"""
Active configuration: {{
    general: {self.general},
    randomClick: {self.randomClick},
    ScreenshotMarkerConfig: [
{chr(10).join(f'        {marker},' for marker in self.ssMarkers)}
    ]
}}"""
