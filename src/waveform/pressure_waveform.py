
import numpy as np
import pandas as pd


def generate_pressure_waveform(
    systolic_bp,
    diastolic_bp,
    n_points=50,
    random_seed=None,
):
    """
    Generate an illustrative synthetic pressure pulse.

    This is a mathematical demonstration, not a validated
    physiological model.
    """
    if systolic_bp <= diastolic_bp:
        raise ValueError(
            "Systolic pressure must exceed diastolic pressure."
        )

    if n_points < 2:
        raise ValueError("n_points must be at least 2.")

    rng = np.random.default_rng(random_seed)

    time = np.linspace(0, 1, n_points, endpoint=False)

    # Pressure rises rapidly, then declines more gradually.
    pulse = np.where(
        time < 0.25,
        time / 0.25,
        (1 - time) / 0.75,
    )

    pulse = np.clip(pulse, 0, 1)

    pressure = (
        diastolic_bp
        + (systolic_bp - diastolic_bp) * pulse
    )

    # Small noise makes the synthetic signal less uniform.
    pressure += rng.normal(0, 0.8, n_points)

    return pd.DataFrame({
        "time": time,
        "pressure": pressure,
    })


def generate_patient_waveforms(
    patients,
    n_points=50,
    random_seed=42,
):
    """Generate illustrative waveforms for all patients."""
    rng = np.random.default_rng(random_seed)
    records = []

    for _, patient in patients.iterrows():
        seed = int(rng.integers(0, 2**31 - 1))

        waveform = generate_pressure_waveform(
            systolic_bp=float(patient["systolic_bp"]),
            diastolic_bp=float(patient["diastolic_bp"]),
            n_points=n_points,
            random_seed=seed,
        )

        for point_number, point in waveform.iterrows():
            records.append({
                "patient_id": patient["patient_id"],
                "class": patient["class"],
                "time": point["time"],
                "pressure": point["pressure"],
            })

    return pd.DataFrame(records)


if __name__ == "__main__":
    example = generate_pressure_waveform(
        systolic_bp=120,
        diastolic_bp=80,
        random_seed=42,
    )

    print("Synthetic pressure waveform preview:")
    print(example.head(10).round(2).to_string(index=False))
    print("\nNumber of time points:", len(example))
    print("Minimum pressure:", round(example["pressure"].min(), 2))
    print("Maximum pressure:", round(example["pressure"].max(), 2))
    
def save_all_patient_waveforms():
    from pathlib import Path

    project_root = Path(__file__).resolve().parents[2]
    patient_file = (
        project_root / "data" / "processed"
        / "synthetic_patients.csv"
    )
    output_file = (
        project_root / "data" / "processed"
        / "patient_waveforms.csv"
    )

    if not patient_file.exists():
        raise FileNotFoundError(
            f"Patient dataset not found: {patient_file}"
        )

    patients = pd.read_csv(patient_file)

    required_columns = [
        "patient_id", "class", "systolic_bp", "diastolic_bp"
    ]
    missing = [
        column for column in required_columns
        if column not in patients.columns
    ]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    waveforms = generate_patient_waveforms(
        patients,
        n_points=50,
        random_seed=42,
    )

    output_file.parent.mkdir(parents=True, exist_ok=True)
    waveforms.to_csv(output_file, index=False)

    print("Patient waveform dataset generated!")
    print("Patients:", patients["patient_id"].nunique())
    print("Total waveform points:", len(waveforms))
    print("Points per patient: 50")
    print("Saved to:", output_file)


if __name__ == "__main__":
    save_all_patient_waveforms()

