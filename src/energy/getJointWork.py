import numpy as np


def get_joint_work(joint_angles: np.ndarray, time_array: np.ndarray) -> float:
    """
    Calculate positive mechanical work from joint angles.
    """
    angular_velocity = np.diff(joint_angles) / np.diff(time_array)
    positive_velocity = np.maximum(angular_velocity, 0)
    delta_t = np.diff(time_array)
    work = np.sum(positive_velocity * delta_t)
    return work
