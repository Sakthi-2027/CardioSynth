
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REFERENCE_FILE = PROJECT_ROOT / "data" / "raw" / "reference_values.csv"

REQUIRED_COLUMNS = {
    "feature",
    "class",
    "distribution",
    "parameter_1",
    "parameter_2",
    "unit",
    "source_type",
    "notes",
}

EXPECTED_CLASSES = {
    "Normal",
    "Hypertension",
    "Arrhythmia",
    "Valve Disorder",
}


def load_reference_data() -> pd.DataFrame:
    """Load and validate the reference parameter table."""
    if not REFERENCE_FILE.exists():
        raise FileNotFoundError(
            f"Reference file not found: {REFERENCE_FILE}"
        )

    data = pd.read_csv(REFERENCE_FILE)

    missing_columns = REQUIRED_COLUMNS - set(data.columns)
    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    if data[list(REQUIRED_COLUMNS)].isnull().any().any():
        # parameter_2 is intentionally blank for some distributions.
        essential_columns = REQUIRED_COLUMNS - {"parameter_2"}
        if data[list(essential_columns)].isnull().any().any():
            raise ValueError("Essential reference fields contain missing values.")

    actual_classes = set(data["class"].unique())
    if actual_classes != EXPECTED_CLASSES:
        raise ValueError(
            f"Unexpected classes. Found: {sorted(actual_classes)}"
        )

    allowed_distributions = {
        "normal",
        "bernoulli",
        "lognormal",
        "categorical",
    }

    invalid_distributions = (
        set(data["distribution"].unique()) - allowed_distributions
    )
    if invalid_distributions:
        raise ValueError(
            f"Unsupported distributions: {sorted(invalid_distributions)}"
        )

    # Check probability parameters for Bernoulli distributions.
    bernoulli_rows = data["distribution"] == "bernoulli"
    probabilities = pd.to_numeric(
        data.loc[bernoulli_rows, "parameter_1"],
        errors="coerce",
    )

    if probabilities.isnull().any() or not probabilities.between(0, 1).all():
        raise ValueError("Bernoulli probabilities must be between 0 and 1.")

    # Check categorical probability lists.
    categorical_rows = data[data["distribution"] == "categorical"]

    for _, row in categorical_rows.iterrows():
        values = [float(x) for x in str(row["parameter_1"]).split(";")]

        if any(value < 0 or value > 1 for value in values):
            raise ValueError(
                f"Invalid categorical probability for {row['feature']} "
                f"({row['class']})."
            )

        if abs(sum(values) - 1.0) > 1e-6:
            raise ValueError(
                f"Categorical probabilities must sum to 1 for "
                f"{row['feature']} ({row['class']})."
            )

    return data


if __name__ == "__main__":
    reference_data = load_reference_data()

    print("Reference data loaded successfully!")
    print(f"Total parameter rows: {len(reference_data)}")
    print(f"Unique features: {reference_data['feature'].nunique()}")
    print(f"Patient classes: {', '.join(sorted(reference_data['class'].unique()))}")
    print("\nFirst five rows:")
    print(reference_data.head().to_string(index=False))
