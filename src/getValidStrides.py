# src/stride_filter.py
import numpy as np


def get_valid_strides(time_array: np.ndarray, heel_strike_indices: np.ndarray, margin_sec: float = 5.0):
    """
    Filters heel strikes to only include those after start+5s and before end-5s.
    Returns (start_index, end_index, stride_count)
    """
    start_time = time_array[0] + margin_sec
    end_time = time_array[-1] - margin_sec

    valid_indices = [i for i in heel_strike_indices if start_time <= time_array[i] <= end_time]

    if len(valid_indices) < 2:
        return None, None, 0

    return valid_indices[0], valid_indices[-1], len(valid_indices) - 1
