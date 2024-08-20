from dataclasses import dataclass
import os
import json
from typing import Any

from .common import get_now
from .logger import get_logger

logger = get_logger(__name__)


@dataclass
class GeneralConfigType:
    DATA_PATH: str
    FILENAME_PREFIX: str
    META_DATA: dict|None = None

    def __post_init__(self):
        self.FILENAME_PREFIX = f"{self.FILENAME_PREFIX}_{get_now(True)}"

    def initialize(self):

        os.makedirs(self.get_full_path())

        if self.META_DATA is not None:
            with open(os.path.join(self.get_full_path(), 'meta.json'), "w+") as f:
                json.dump(self.META_DATA, f, indent=2)

    def get_full_path(self):
        return os.path.join(self.DATA_PATH, self.FILENAME_PREFIX)


@dataclass
class Factory:
    CLASS: type
    CONFIG: Any


@dataclass
class ConfigType:
    general: GeneralConfigType
    recorders: list[Factory]
    triggers: list[Factory]

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
