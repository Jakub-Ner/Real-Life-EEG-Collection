from dataclasses import dataclass
from typing import Any

from .common import get_now
from .logger import get_logger

logger = get_logger(__name__)


@dataclass
class GeneralConfigType:
    DATA_PATH: str
    FILENAME_PREFIX: str

    def __post_init__(self):
        self.FILENAME_PREFIX = f"{self.FILENAME_PREFIX}_{get_now(True)}"


@dataclass
class FactoryType:
    CLASS: type
    CONFIG: Any


@dataclass
class ConfigType:
    general: GeneralConfigType
    recorders: list[FactoryType]
    triggers: list[FactoryType]

    # def __post_init__(self):
    #     logger.info(self)

    def __repr__(self) -> str:
        return f"""
Active configuration: {{
    general: {self.general},
    recorders: {self.recorders},
    triggers: [
{chr(10).join(f'        {marker},' for marker in self.triggers)}
    ]
}}"""
