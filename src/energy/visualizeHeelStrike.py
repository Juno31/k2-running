import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")  # 또는 QtAgg

def plot_heel_strikes_with_valid_range(time, rheel_z, heel_strikes, valid_heel_strikes, start_idx, end_idx, title):
    plt.figure(figsize=(12, 5))
    plt.plot(time, rheel_z, label="RHeel_Z", color="blue")
    plt.plot(time[heel_strikes], rheel_z[heel_strikes], "ro", label="Heel Strikes")

    if start_idx is not None and end_idx is not None:
        plt.axvspan(time[start_idx], time[end_idx], color='orange', alpha=0.3, label="Valid Stride Range")
        plt.plot(time[valid_heel_strikes], rheel_z[valid_heel_strikes], "go", label="Valid Heel Strikes")

    plt.title(f"Valid Stride Detection: {title}")
    plt.xlabel("Time (s)")
    plt.ylabel("RHeel_Z (cm)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()