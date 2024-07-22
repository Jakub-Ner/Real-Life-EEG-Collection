import os
from src.utils.constants import DATA_PATH
from .utils.UDPStreamer import UDPStreamer
from .utils.config_helpers import FORMAT, EEGConfigType, UDPConfigType

udp_streamer = UDPConfigType(
    IP="127.0.0.1",
    PORT=1000,
    CONNECTION_TIMEOUT=4,  # in seconds
    BUFFER_BYTE_SIZE=1024,
    CLASS=UDPStreamer,
    COL_SEPARATOR=",",
    OUTPUT_FORMAT=FORMAT.ASCII,
)

CONFIG = EEGConfigType(streamer=udp_streamer, EEG_PATH=os.path.join(DATA_PATH, "eeg"))
