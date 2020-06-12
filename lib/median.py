import numpy as np


def median(arr):
  # default value is 1
  return np.median(np.array(arr)) if len(arr) != 0 else 1