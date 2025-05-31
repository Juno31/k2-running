# main.py
import pandas as pd
from src.common import detect_heel_strike_from_y, get_valid_strides
from src.energy import get_joint_work, make_energy_report
from src.consistency import get_joint_sample_entropy, make_consistency_report

# Define datasets
raw_datasets = [
    ("crocs", "data/raw/crocs_mot.xlsx", "data/raw/crocs_marker.xlsx"),
    ("performance", "data/raw/performance_mot.xlsx", "data/raw/performance_marker.xlsx"),
    ("sneakers", "data/raw/sneakers_mot.xlsx", "data/raw/sneakers_marker.xlsx")
]


def main():
    energy_report_data = []
    consistency_report_data = []

    for name, mot_path, marker_path in raw_datasets:
        print(f"\nStart Processing: {name}")

        # Prepare data
        mot_df = pd.read_excel(mot_path)
        marker_df = pd.read_excel(marker_path)

        # Get heel strike
        time = marker_df["Time"].to_numpy()
        rheel_y = marker_df["RHeel_Y"].to_numpy()
        heel_strikes = detect_heel_strike_from_y(rheel_y)

        # Get valid stride range
        start_idx, end_idx, stride_count = get_valid_strides(time, heel_strikes)
        if stride_count == 0:
            print("No valid strides found. Skipping dataset.")
            continue

        # Prepare calculation parameters
        valid_time = mot_df["time"].to_numpy()[start_idx:end_idx]
        target_joints = [
            "hip_flexion_r",
            "knee_angle_r",
            "ankle_angle_r",
        ]

        # Calculate average mechanical work per stride
        total_work = 0

        for joint in target_joints:
            joint_data = mot_df[joint].to_numpy()[start_idx:end_idx]
            joint_work = get_joint_work(joint_data, valid_time)
            total_work += joint_work

        avg_work_per_stride = total_work / stride_count

        # Calculate ankle_angle_r sample entropy
        joint_data = mot_df['ankle_angle_r'].to_numpy()[start_idx:end_idx]
        embedding_dimension = int((end_idx - start_idx) / stride_count)
        entropy_results = get_joint_sample_entropy(joint_data, m=embedding_dimension, r_ratio=0.15)

        # Print result
        print(f"Valid strides: {stride_count}")
        print(f"Average work per stride: {avg_work_per_stride:.3f}")
        print(f"Sample Entropy: {entropy_results}")
        print(f"Embedding Dimension: {embedding_dimension}\n")

        # Save data for report
        energy_report_data.append({
            "name": name,
            "stride_count": stride_count,
            "avg_work": avg_work_per_stride,
            "time": time,
            "rheel_y": rheel_y,
            "heel_strikes": heel_strikes,
            "start_idx": start_idx,
            "end_idx": end_idx
        })

        consistency_report_data.append({
            "name": name,
            "stride_count": stride_count,
            "sample_entropy": entropy_results,
            "time": time,
            "ankle_angle_r": mot_df["ankle_angle_r"].to_numpy(),
            "start_idx": start_idx,
            "end_idx": end_idx
        })

    # Generate PDF report
    make_energy_report(energy_report_data, output_path="./output/energy_efficiency.pdf")
    make_consistency_report(consistency_report_data, output_path="./output/consistency.pdf")



if __name__ == '__main__':
    main()
