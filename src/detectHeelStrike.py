import numpy as np
from scipy.signal import find_peaks


def detect_heel_strike_from_z(z_array: np.ndarray, distance: int = 30) -> np.ndarray:
    """
    Detect heel strikes based on local minima of RHeel_Z.
    """
    inverted_z = -z_array
    peaks, _ = find_peaks(inverted_z, distance=distance)
    return peaks
