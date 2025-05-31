import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def make_consistency_report(report_data: list, output_path="consistency_report.pdf"):
    """
    Sample Entropy 기반 러닝 패턴 일관성 리포트 PDF로 저장

    Parameters:
        report_data: list of dict with keys:
            - name, stride_count, sample_entropy, start_idx, end_idx, time, ankle_angle_r
        output_path: PDF 저장 경로
    """
    with PdfPages(output_path) as pdf:
        for entry in report_data:
            name = entry["name"]
            stride_count = entry["stride_count"]
            sample_entropy = entry["sample_entropy"]
            time = entry["time"]
            ankle_angle_r = entry["ankle_angle_r"]
            start_idx = entry["start_idx"]
            end_idx = entry["end_idx"]

            fig, ax = plt.subplots(figsize=(12, 5))
            ax.plot(time, ankle_angle_r, label="ankle_angle_r", color="blue")
            ax.axvspan(time[start_idx], time[end_idx], color="orange", alpha=0.3, label="Valid Range")

            ax.set_title(f"{name} - Valid Strides: {stride_count}, Sample Entropy: {sample_entropy:.4f}")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("ankle_angle_r (deg)")
            ax.legend()
            ax.grid(True)
            plt.tight_layout()
            pdf.savefig(fig)
            plt.close(fig)

    return output_path
