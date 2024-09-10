import numpy as np


class Buffer:
  def __init__(self, size):
    self.array = np.zeros(size * 2)
    self.half = size
    self.pointer = 0

  def add(self, row: np.ndarray):
    ...

  def get(self):
    ...