from src.recorders.screen.config_helpers import ScreenConfig
from src.recorders.screen.ScreenRecorder import ScreenRecorder

from src.recorders.camera.CameraRecorder import CameraRecorder
from src.recorders.camera.config_helpers import CameraConfig

from src.recorders.eeg_lsl.config_helpers import EegLslConfig
from src.recorders.eeg_lsl.EegLSLRecorder import EegLSLRecorder

from src.recorders.eeg_udp.EegUdpRecorder import EegUdpRecorder
from src.recorders.eeg_udp.config_helpers import FORMAT, EegUdpConfig
from src.utils.config_helpers import (
    ConfigType,
    Factory,
    GeneralConfigType,
)


from src.triggers.randomClick.config_helpers import RandomClickConfig
from src.triggers.randomClick.RandomClick import RandomClick

from src.triggers.screenshotMarker.config_helpers import ScreenshotMarkerConfig
from src.triggers.screenshotMarker.ScreenshotMarker import ScreenshotMarker

general_config = GeneralConfigType(
    DATA_PATH="./data",
    FILENAME_PREFIX="lol",
    META_DATA={
        'markers': {
            '0': 'none',
            '1': 'kill',
            '2': 'death',
            '3': 'random flash',
        },
        'subject': 'subject_1',
    }
)

eeg_udp_config = EegUdpConfig(
    IP="127.0.0.1",
    PORT=1000,
    DATA_PATH=general_config.get_full_path(),
    FILENAME="eeg.csv",
    CONNECTION_TIMEOUT=4,  # in seconds
    BUFFER_BYTE_SIZE=1024,
    COL_SEPARATOR=",",
    OUTPUT_FORMAT=FORMAT.ASCII,
)

eeg_lsl_config = EegLslConfig(
    STREAM_NAME="Cortex PSD",
    DATA_PATH=general_config.get_full_path(),
    FILENAME="eeg_lsl.jsonl",
)

camera_config = CameraConfig(
    DATA_PATH=general_config.get_full_path(),
    FILENAME="camera.avi",
    DURATION=2.0,
)

screen_config = ScreenConfig(
    DATA_PATH=general_config.get_full_path(),
    FILENAME="screen.avi",
)

recorders = [
    #Factory(CLASS=EegUdpRecorder, CONFIG=eeg_udp_config),
    Factory(CLASS=EegLSLRecorder, CONFIG=eeg_lsl_config),
    Factory(CLASS=CameraRecorder, CONFIG=camera_config),
    Factory(CLASS=ScreenRecorder, CONFIG=screen_config),
]

triggers = [
    Factory(
        CLASS=RandomClick,
        CONFIG=RandomClickConfig(
            KEY="d", 
            MARKER='3',
            RANDOM_RANGE=range(300, 350, 1),
            DEATH_AREA_TOP=(570, 962),
            DEATH_AREA_BOTTOM=(619, 984),
        ),
    ),
    Factory(
        CLASS=ScreenshotMarker,
        CONFIG=ScreenshotMarkerConfig(
            TOP=(1637, 0),
            BOTTOM=(1678, 25),
            MARKER="1", # kill event
            EVENT_NAME=general_config.META_DATA['markers']['1'],
            DELAY_S=0.1,
            DATA_PATH=general_config.get_full_path(),
        ),
    ),
    Factory(
        CLASS=ScreenshotMarker,
        CONFIG=ScreenshotMarkerConfig(
            TOP=(1680, 0),
            BOTTOM=(1705, 25),
            MARKER="2", # death event
            EVENT_NAME=general_config.META_DATA['markers']['2'],
            DELAY_S=0.1,
            DATA_PATH=general_config.get_full_path(),
        ),
    ),
]

CONFIG = ConfigType(
    general=general_config,
    recorders=recorders,
    triggers=triggers,
)
