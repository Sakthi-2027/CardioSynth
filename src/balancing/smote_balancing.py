
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from imblearn.over_sampling import SMOTENC


ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = ROOT / "data" / "processed" / "synthetic_patients.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "smote_experiment.csv"
PLOT_FILE = ROOT / "outputs" / "plots" / "smote_before_after.png"


def run_smote_experiment():
    print("\n" + "=" * 55)
    print("CARDIOSYNTH — SMOTENC BALANCING EXPERIMENT")
    print("=" * 55)

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {INPUT_FILE}\nRun python main.py first."
        )

    data = pd.read_csv(INPUT_FILE)

    # Create an intentionally imbalanced experimental subset.
    # The original dataset is never modified.
    minority_class = "Arrhythmia"
    minority_data = data[data["class"] == minority_class].sample(
        n=100, random_state=42
    )

    other_data = data[data["class"] != minority_class]

    experiment_data = pd.concat(
        [other_data, minority_data], ignore_index=True
    )

    X = experiment_data.drop(columns=["patient_id", "class"])
    y = experiment_data["class"]

    print("\nClass counts before SMOTENC:")
    print(y.value_counts().sort_index())

    categorical_features = [
        "sex",
        "fasting_blood_sugar",
        "exercise_angina",
        "chest_pain_type",
        "major_vessels",
    ]

    sampler = SMOTENC(
        categorical_features=categorical_features,
        random_state=42,
        k_neighbors=5,
    )

    X_resampled, y_resampled = sampler.fit_resample(X, y)

    balanced_data = X_resampled.copy()
    balanced_data["class"] = y_resampled

    # Give all experimental rows unique IDs.
    balanced_data.insert(
        0,
        "patient_id",
        [f"SMOTE_{i + 1:05d}" for i in range(len(balanced_data))],
    )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    PLOT_FILE.parent.mkdir(parents=True, exist_ok=True)

    balanced_data.to_csv(OUTPUT_FILE, index=False)

    before_counts = y.value_counts().sort_index()
    after_counts = y_resampled.value_counts().sort_index()

    print("\nClass counts after SMOTENC:")
    print(after_counts)

    # Visual comparison for viva.
    classes = before_counts.index.tolist()
    x_positions = list(range(len(classes)))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(
        [x - width / 2 for x in x_positions],
        [before_counts[c] for c in classes],
        width,
        label="Before SMOTENC",
    )

    ax.bar(
        [x + width / 2 for x in x_positions],
        [after_counts[c] for c in classes],
        width,
        label="After SMOTENC",
    )

    ax.set_title("CardioSynth: Class Distribution Before and After SMOTENC")
    ax.set_xlabel("Patient class")
    ax.set_ylabel("Number of records")
    ax.set_xticks(x_positions)
    ax.set_xticklabels(classes, rotation=15)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    fig.tight_layout()
    fig.savefig(PLOT_FILE, dpi=300)
    plt.close(fig)

    print(f"\nExperimental dataset saved to: {OUTPUT_FILE}")
    print(f"Comparison chart saved to: {PLOT_FILE}")
    print("\nOriginal synthetic_patients.csv remains unchanged.")
    print(
        "Note: SMOTENC creates interpolated examples from synthetic data; "
        "it does not establish clinical validity."
    )


if __name__ == "__main__":
    run_smote_experiment()

