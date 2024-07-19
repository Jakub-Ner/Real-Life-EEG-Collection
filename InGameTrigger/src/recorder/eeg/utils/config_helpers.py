from dataclasses import dataclass
import os

from src.utils.constants import DATA_PATH
from src.utils.logger import get_logger

from .helpers import StreamerConfig

logger = get_logger(__name__)


@dataclass
class UDPConfiguration(StreamerConfig):
    IP: str
    PORT: int
    CONNECTION_TIMEOUT: int = 2  # in seconds
    BUFFER_BYTE_SIZE: int = 1024
    CLASS: type  # class to be instantiated


@dataclass
class EEGConfiguration:
    streamer: StreamerConfig
    EEG_PATH: str = os.path.join(DATA_PATH, "eeg")

    def __post_init__(self):
        logger.info(self)

    def __repr__(self) -> str:
        return f"""
EEG Recorder configuration: {{
    EEG_PATH: {self.EEG_PATH},
    streamer: {self.streamer}
}}"""
