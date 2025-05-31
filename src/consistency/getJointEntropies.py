import pandas as pd

def get_joint_entropies(df: pd.DataFrame, start_idx: int, end_idx: int) -> dict:
    """
    Compute sample entropy for 3 joint angles within valid stride range.
    Parameters:
        df: DataFrame containing joint angle columns
        start_idx: start index of valid stride
        end_idx: end index of valid stride
    Returns:
        Dictionary with sample entropies
    """
    joints = ['hip_flexion_r', 'knee_angle_r', 'ankle_angle_r']
    entropy_results = {}

    for joint in joints:
        series = df[joint].to_numpy()[start_idx:end_idx]
        entropy = compute_sample_entropy(series, m=2, r_ratio=0.2)
        entropy_results[joint] = entropy

    return entropy_results
