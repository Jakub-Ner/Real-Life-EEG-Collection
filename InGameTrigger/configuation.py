from src.recorders.eeg_udp.EegUdpRecorder import EegUdpRecorder
from src.recorders.eeg_udp.config_helpers import FORMAT, UDPConfigType
from src.utils.config_helpers import (
    ConfigType,
    FactoryType,
    GeneralConfigType,
)
from src.triggers.randomClick.RandomClick import RandomClick
from src.triggers.randomClick.config_helpers import RandomClickConfigType
from src.triggers.screenshotMarker.config_helpers import ScreenshotMarkerConfigType
from src.triggers.screenshotMarker.ScreenshotMarker import ScreenshotMarker

general_config = GeneralConfigType(
    DATA_PATH="./data",
    FILENAME_PREFIX="lol",
)

eeg_udp_config = UDPConfigType(
    IP="127.0.0.1",
    PORT=1000,
    OUT_PATH=general_config.DATA_PATH,
    FILENAME=general_config.FILENAME_PREFIX,
    CONNECTION_TIMEOUT=4,  # in seconds
    BUFFER_BYTE_SIZE=1024,
    COL_SEPARATOR=",",
    OUTPUT_FORMAT=FORMAT.ASCII,
)

recorders = [
    FactoryType(
        CLASS=EegUdpRecorder,
        CONFIG=eeg_udp_config,
    ),
]

triggers = [
    FactoryType(
        CLASS=RandomClick,
        CONFIG=RandomClickConfigType(KEY="d", RANDOM_RANGE=(300, 320, 1)),
    ),
    FactoryType(
        CLASS=ScreenshotMarker,
        CONFIG=ScreenshotMarkerConfigType(
            TOP=(1637, 0), BOTTOM=(1678, 25), MARKER="kill", DELAY_S=0.1
        ),
    ),
    FactoryType(
        CLASS=ScreenshotMarker,
        CONFIG=ScreenshotMarkerConfigType(
            TOP=(1680, 0), BOTTOM=(1705, 25), MARKER="death", DELAY_S=0.1
        ),
    ),
]

CONFIG = ConfigType(
    general=general_config,
    recorders=recorders,
    triggers=triggers,
)
