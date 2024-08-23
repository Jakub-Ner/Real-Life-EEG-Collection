from dataclasses import dataclass
from enum import Enum

from src.utils.logger import get_logger

logger = get_logger(__name__)


class FORMAT(Enum):
    BINARY = "binary"
    ASCII = "ascii"


@dataclass
class EegLslConfig:
    STREAM_NAME: str
    DATA_PATH: str
    FILENAME: str
    CHUNK_SIZE: int = 5
    PULL_TIMEOUT: int = 1  # in seconds
    OUTPUT_FORMAT: FORMAT = FORMAT.ASCII

