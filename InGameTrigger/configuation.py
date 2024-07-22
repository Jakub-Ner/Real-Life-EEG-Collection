from src.utils.config_helpers import (
    ConfigType,
    GeneralConfigType,
    ScreenshotMarkerConfigType,
    RandomClickConfigType,
)

generalConfig = GeneralConfigType(
    FILENAME_PREFIX="lol",
)

randomClickConfig = RandomClickConfigType(
    KEY="d",
    STATE_DURATION=5,
    RANDOM_RANGE=(300, 320, 1),
)

ssMarkers = [
    ScreenshotMarkerConfigType(
        TOP=(1637, 0), BOTTOM=(1678, 25), MARKER="kill", DELAY_S=0.1
    ),
    ScreenshotMarkerConfigType(
        TOP=(1680, 0), BOTTOM=(1705, 25), MARKER="death", DELAY_S=0.1
    ),
]

CONFIG = ConfigType(
    general=generalConfig,
    randomClick=randomClickConfig,
    ssMarkers=ssMarkers,
)
