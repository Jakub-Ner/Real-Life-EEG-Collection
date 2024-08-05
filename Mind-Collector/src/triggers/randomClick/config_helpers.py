from dataclasses import dataclass


@dataclass
class RandomClickConfig:
    KEY: str
    RANDOM_RANGE: range  # (start, stop, step)
