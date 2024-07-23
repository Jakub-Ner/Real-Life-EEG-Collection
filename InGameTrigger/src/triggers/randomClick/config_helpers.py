from dataclasses import dataclass


@dataclass
class RandomClickConfig:
    KEY: str
    RANDOM_RANGE: tuple[int, int, int]  # (start, stop, step)
