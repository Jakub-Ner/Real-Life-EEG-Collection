from src.utils.config_helpers import (
    Config,
    GeneralConfig,
    ScreenshotMarkerConfig,
    RandomClickConfig,
)

generalConfig = GeneralConfig(
    FILENAME_PREFIX="lol",
)

randomClickConfig = RandomClickConfig(
    KEY="d",
    STATE_DURATION=5,
    RANDOM_RANGE=(300, 320, 1),
)

ssMarkers = [
    ScreenshotMarkerConfig(
        TOP=(1637, 0), BOTTOM=(1730, 25), MARKER="death", DELAY_S=0.1
    ),
    ScreenshotMarkerConfig(
        TOP=(1637, 0), BOTTOM=(1730, 25), MARKER="kill", DELAY_S=0.1
    ),
]

CONFIG = Config(
    general=generalConfig,
    randomClick=randomClickConfig,
    # ssMarkers=ssMarkers,
)
