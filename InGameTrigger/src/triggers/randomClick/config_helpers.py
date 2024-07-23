from dataclasses import dataclass


@dataclass
class RandomClickConfigType:
    KEY: str
    RANDOM_RANGE: tuple[int, int, int]  # (start, stop, step)
