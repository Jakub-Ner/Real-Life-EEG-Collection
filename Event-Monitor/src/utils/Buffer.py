import numpy as np


class Buffer:
  def __init__(self, shape: tuple[int, int]):
    self.array = np.zeros(shape)
    self.size = shape[0]
    self.pointer = 0

  def add(self, row: np.ndarray):
    self.array[self.pointer] = row
    self.pointer = (self.pointer + 1) % self.size

  def get(self):
    return np.vstack((self.array[self.pointer:], self.array[:self.pointer]))
  
  def __len__(self):
    return self.size