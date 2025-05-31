import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def make_report(report_data, output_path="comparison_report.pdf"):
    with PdfPages(output_path) as pdf:
        for entry in report_data:
            name = entry["name"]
            stride_count = entry["stride_count"]
            avg_work = entry["avg_work"]
            time = entry["time"]
            rheel_y = entry["rheel_y"]
            heel_strikes = entry["heel_strikes"]
            start_idx = entry["start_idx"]
            end_idx = entry["end_idx"]

            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(time, rheel_y, label="RHeel_Y", color="blue")
            ax.plot(time[heel_strikes], rheel_y[heel_strikes], "ro", label="Heel Strikes")
            valid_strikes = [idx for idx in heel_strikes if start_idx <= idx <= end_idx]
            ax.plot(time[valid_strikes], rheel_y[valid_strikes], "go", label="Valid Heel Strikes")
            ax.axvspan(time[start_idx], time[end_idx], color="orange", alpha=0.2, label="Valid Range")

            ax.set_title(f"{name} - Valid Strides: {stride_count}, Avg Work: {avg_work:.3f}")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("RHeel_Y (cm)")
            ax.legend()
            ax.grid(True)
            plt.tight_layout()
            pdf.savefig(fig)
            plt.close(fig)

    return output_path
