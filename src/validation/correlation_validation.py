
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "processed" / "synthetic_patients.csv"
OUTPUT_FILE = PROJECT_ROOT / "outputs" / "reports" / "correlation_validation.csv"

FEATURES = [
    "age",
    "systolic_bp",
    "diastolic_bp",
    "heart_rate",
    "max_heart_rate",
    "cholesterol",
    "st_depression",
]


def validate_correlations(data):
    """Report generated correlations and basic matrix diagnostics."""
    missing = set(FEATURES) - set(data.columns)
    if missing:
        raise ValueError(f"Missing features: {sorted(missing)}")

    correlation = data[FEATURES].corr(method="pearson")
    records = []

    for i, feature_a in enumerate(FEATURES):
        for feature_b in FEATURES[i + 1:]:
            records.append({
                "feature_a": feature_a,
                "feature_b": feature_b,
                "pearson_correlation": correlation.loc[
                    feature_a, feature_b
                ],
            })

    result = pd.DataFrame(records)

    matrix = correlation.to_numpy()
    eigenvalues = np.linalg.eigvalsh(matrix)

    print("CORRELATION VALIDATION")
    print("=" * 50)
    print("\nGenerated Pearson correlation matrix:")
    print(correlation.round(2).to_string())

    print("\nMatrix checks:")
    print(f"Symmetric: {np.allclose(matrix, matrix.T)}")
    print(
        "Unit diagonal: "
        f"{np.allclose(np.diag(matrix), 1.0)}"
    )
    print(f"Minimum eigenvalue: {eigenvalues.min():.6f}")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_FILE, index=False)
    print(f"\nPairwise results saved to: {OUTPUT_FILE}")

    return result


if __name__ == "__main__":
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}. "
            "Generate the dataset first."
        )

    dataset = pd.read_csv(DATA_FILE)
    validate_correlations(dataset)
