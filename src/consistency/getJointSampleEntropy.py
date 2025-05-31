import numpy as np


def get_joint_sample_entropy(x: np.ndarray, m: int = 2, r_ratio: float = 0.2) -> float:
    n = len(x)
    r = r_ratio * np.std(x)

    def _phi(m):
        patterns = np.array([x[i:i + m] for i in range(n - m + 1)])
        count = 0
        for i in range(len(patterns)):
            dist = np.max(np.abs(patterns - patterns[i]), axis=1)
            count += np.sum(dist <= r) - 1  # subtract self-match
        return count

    B = _phi(m)
    A = _phi(m + 1)

    # avoid log(0)
    if B == 0 or A == 0:
        return np.inf

    return -np.log(A / B)