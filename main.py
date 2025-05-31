# main.py
import pandas as pd
from src import detect_heel_strike_from_y, get_valid_strides, get_joint_work, plot_heel_strikes_with_valid_range, make_report

# Define datasets
mot_files = [
    ("crocs", "data/raw/crocs_mot.xlsx", "data/raw/crocs_marker.xlsx"),
    ("performance", "data/raw/performance_mot.xlsx", "data/raw/performance_marker.xlsx"),
    ("sneakers", "data/raw/sneakers_mot.xlsx", "data/raw/sneakers_marker.xlsx")
]


def main():
    report_data = []

    for name, mot_path, marker_path in mot_files:
        print(f"\nProcessing: {name}")

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
        total_work = 0
        target_joints = [
            "hip_flexion_r",
            "knee_angle_r",
            "ankle_angle_r",
        ]

        # Calculate average mechanical work per stride
        for joint in target_joints:
            joint_data = mot_df[joint].to_numpy()[start_idx:end_idx]
            joint_work = get_joint_work(joint_data, valid_time)
            total_work += joint_work

        avg_work_per_stride = total_work / stride_count

        # Print result
        print(f"Valid strides: {stride_count}")
        print(f"Average work per stride: {avg_work_per_stride:.3f}\n")

        # Visualize analyze range
        # valid_heel_strikes = [idx for idx in heel_strikes if start_idx <= idx <= end_idx]
        # plot_heel_strikes_with_valid_range(
        #     time, rheel_y, heel_strikes, valid_heel_strikes, start_idx, end_idx, title=name
        # )

        # Save data for report
        report_data.append({
            "name": name,
            "stride_count": stride_count,
            "avg_work": avg_work_per_stride,
            "time": time,
            "rheel_y": rheel_y,
            "heel_strikes": heel_strikes,
            "start_idx": start_idx,
            "end_idx": end_idx
        })

    # Generate PDF report
    make_report(report_data, output_path="./output/energy_efficiency.pdf")


if __name__ == '__main__':
    main()
