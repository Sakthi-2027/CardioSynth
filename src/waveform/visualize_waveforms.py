
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_ROOT / "data" / "processed"
    / "patient_waveforms.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT / "outputs" / "plots"
    / "sample_pressure_waveforms.png"
)


def visualize_waveforms():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Waveform dataset not found: {DATA_FILE}"
        )

    data = pd.read_csv(DATA_FILE)

    classes = [
        "Normal",
        "Hypertension",
        "Arrhythmia",
        "Valve Disorder",
    ]

    fig, axes = plt.subplots(
        2, 2, figsize=(12, 8), sharex=True
    )

    for ax, patient_class in zip(axes.flatten(), classes):
        patient = data[data["class"] == patient_class]

        if patient.empty:
            ax.set_title(f"{patient_class}: no data")
            continue

        patient_id = patient["patient_id"].iloc[0]
        waveform = patient[patient["patient_id"] == patient_id]

        ax.plot(
            waveform["time"],
            waveform["pressure"],
        )
        ax.set_title(f"{patient_class} (sample patient)")
        ax.set_xlabel("Normalized time")
        ax.set_ylabel("Synthetic pressure (mmHg)")
        ax.grid(True, alpha=0.3)

    fig.suptitle(
        "CardioSynth — Illustrative Synthetic Pressure Waveforms"
    )
    fig.tight_layout()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_FILE, dpi=150)
    plt.close(fig)

    print("Waveform plots generated successfully!")
    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    visualize_waveforms()

