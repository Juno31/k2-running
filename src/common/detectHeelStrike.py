import numpy as np
from scipy.signal import find_peaks


def detect_heel_strike_from_y(y_array: np.ndarray, distance: int = 30) -> np.ndarray:

    inverted_y = -y_array
    peaks, _ = find_peaks(inverted_y, distance=distance)
    return peaks
