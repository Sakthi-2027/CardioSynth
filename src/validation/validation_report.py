
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "processed" / "synthetic_patients.csv"

EXPECTED_CLASSES = {
    "Normal",
    "Hypertension",
    "Arrhythmia",
    "Valve Disorder",
}

BOUNDS = {
    "age": (18, 100),
    "systolic_bp": (70, 250),
    "diastolic_bp": (40, 150),
    "heart_rate": (30, 220),
    "max_heart_rate": (40, 220),
    "cholesterol": (80, 500),
    "st_depression": (0, 10),
}

BINARY_FEATURES = [
    "sex",
    "fasting_blood_sugar",
    "exercise_angina",
]

CATEGORICAL_LIMITS = {
    "chest_pain_type": 3,
    "major_vessels": 3,
}


def validate_dataset():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    data = pd.read_csv(DATA_FILE)
    issues = []

    def check(condition, success_message, failure_message):
        if condition:
            print(f"[PASS] {success_message}")
        else:
            print(f"[FAIL] {failure_message}")
            issues.append(failure_message)

    print("=" * 55)
    print("CARDIOSYNTH — DATA QUALITY VALIDATION")
    print("=" * 55)

    check(
        len(data) == 2000,
        f"Expected 2000 records; found {len(data)}.",
        f"Expected 2000 records; found {len(data)}.",
    )

    check(
        data["patient_id"].is_unique,
        "Patient IDs are unique.",
        "Duplicate patient IDs found.",
    )

    check(
        not data.isnull().any().any(),
        "No missing values found.",
        "Missing values exist in the dataset.",
    )

    actual_classes = set(data["class"].unique())
    check(
        actual_classes == EXPECTED_CLASSES,
        "All four expected classes are present.",
        f"Unexpected class set: {actual_classes}",
    )

    counts = data["class"].value_counts()
    check(
        len(counts) == 4 and (counts == 500).all(),
        "Each class contains exactly 500 patients.",
        f"Unexpected class counts: {counts.to_dict()}",
    )

    print("\n--- Feature range checks ---")

    for feature, (lower, upper) in BOUNDS.items():
        valid = data[feature].between(lower, upper).all()
        check(
            valid,
            f"{feature} is within [{lower}, {upper}].",
            f"{feature} contains values outside [{lower}, {upper}].",
        )

    print("\n--- Binary feature checks ---")

    for feature in BINARY_FEATURES:
        valid = set(data[feature].dropna().unique()).issubset({0, 1})
        check(
            valid,
            f"{feature} contains only 0 and 1.",
            f"{feature} contains invalid binary values.",
        )

    print("\n--- Categorical feature checks ---")

    for feature, maximum in CATEGORICAL_LIMITS.items():
        values = data[feature]
        valid = (
            values.notna().all()
            and values.between(0, maximum).all()
            and (values % 1 == 0).all()
        )
        check(
            valid,
            f"{feature} contains valid integer categories.",
            f"{feature} contains invalid categories.",
        )

    # A physiological consistency check, not a diagnosis.
    systolic_greater_than_diastolic = (
        data["systolic_bp"] > data["diastolic_bp"]
    )
    inconsistent_count = int((~systolic_greater_than_diastolic).sum())

    if inconsistent_count == 0:
        print("[PASS] Systolic BP exceeds diastolic BP in every record.")
    else:
        print(
            f"[WARN] {inconsistent_count} records have systolic BP "
            "less than or equal to diastolic BP."
        )
        print("       Review the sampling logic before finalizing the dataset.")

    print("\n--- Descriptive statistics ---")
    numeric_features = list(BOUNDS.keys())
    print(data[numeric_features].describe().round(2).to_string())

    print("\n--- Final result ---")
    if not issues:
        print("All mandatory data-quality checks passed.")
    else:
        print(f"{len(issues)} mandatory check(s) failed.")
        for issue in issues:
            print(f" - {issue}")

    return data, issues


if __name__ == "__main__":
    validate_dataset()
