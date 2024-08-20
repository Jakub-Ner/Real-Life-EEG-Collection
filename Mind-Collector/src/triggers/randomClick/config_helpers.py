from dataclasses import dataclass


@dataclass
class RandomClickConfig:
    KEY: str
    MARKER: str
    RANDOM_RANGE: range  # (start, stop, step)
