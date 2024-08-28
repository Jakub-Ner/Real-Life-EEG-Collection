from dataclasses import dataclass


@dataclass
class RandomClickConfig:
    KEY: str
    MARKER: str
    RANDOM_RANGE: range  # (start, stop, step)
    DEATH_AREA_TOP: tuple[int, int] | None = None
    DEATH_AREA_BOTTOM: tuple[int, int] | None = None
