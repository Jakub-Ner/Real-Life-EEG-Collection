from dataclasses import dataclass
from enum import Enum

from src.utils.logger import get_logger

logger = get_logger(__name__)


class FORMAT(Enum):
    BINARY = "binary"
    ASCII = "ascii"


@dataclass
class UDPConfigType:
    IP: str
    PORT: int
    OUT_PATH: str
    FILENAME: str
    CONNECTION_TIMEOUT: int = 4  # in seconds
    BUFFER_BYTE_SIZE: int = 1024
    COL_SEPARATOR: str = ","
    OUTPUT_FORMAT: FORMAT = FORMAT.ASCII
