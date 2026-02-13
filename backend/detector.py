import numpy as np

def detect_thrashing(loads, faults):
    diff = np.diff(faults)
    idx = diff.argmax() + 1
    return loads[idx]
