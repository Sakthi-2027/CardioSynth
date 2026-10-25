
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = (
    PROJECT_ROOT / "data" / "processed"
    / "patient_waveforms.csv"
)


def validate_waveforms():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}"
        )

    data = pd.read_csv(DATA_FILE)

    required = [
        "patient_id", "class", "time", "pressure"
    ]

    assert all(col in data.columns for col in required), (
        "Required columns are missing."
    )
    assert not data[required].isnull().any().any(), (
        "Missing values found."
    )

    points_per_patient = data.groupby("patient_id").size()

    assert len(points_per_patient) == 2000, (
        f"Expected 2000 patients, found {len(points_per_patient)}."
    )
    assert (points_per_patient == 50).all(), (
        "Some patients do not have exactly 50 points."
    )

    assert data["pressure"].notna().all()
    assert data["pressure"].between(0, 300).all(), (
        "Pressure values outside the configured sanity-check range."
    )

    print("CARDIOSYNTH — WAVEFORM VALIDATION")
    print("=" * 45)
    print("[PASS] Required columns are present.")
    print("[PASS] No missing values.")
    print("[PASS] Exactly 2000 patients.")
    print("[PASS] Exactly 50 points per patient.")
    print("[PASS] Pressure values within the configured bounds.")
    print("Total waveform points:", len(data))
    print("Classes:", sorted(data["class"].unique()))
    print("\nAll waveform data-quality checks passed.")


if __name__ == "__main__":
    validate_waveforms()
