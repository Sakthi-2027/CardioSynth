
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import kstest, norm, lognorm

from src.generation.reference_data import load_reference_data


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "processed" / "synthetic_patients.csv"
OUTPUT_FILE = PROJECT_ROOT / "outputs" / "reports" / "ks_validation.csv"

NUMERICAL_FEATURES = [
    "age",
    "systolic_bp",
    "diastolic_bp",
    "heart_rate",
    "max_heart_rate",
    "cholesterol",
    "st_depression",
]

ALPHA = 0.05


def run_ks_validation():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    data = pd.read_csv(DATA_FILE)
    reference = load_reference_data()
    results = []

    for patient_class in sorted(data["class"].unique()):
        class_data = data[data["class"] == patient_class]
        class_reference = reference[
            reference["class"] == patient_class
        ]

        for feature in NUMERICAL_FEATURES:
            parameter_rows = class_reference[
                class_reference["feature"] == feature
            ]

            if parameter_rows.empty:
                continue

            parameter = parameter_rows.iloc[0]
            values = class_data[feature].dropna().to_numpy(dtype=float)

            distribution = parameter["distribution"]
            p1 = float(parameter["parameter_1"])
            p2 = float(parameter["parameter_2"])

            if len(values) == 0:
                continue

            if distribution == "normal":
                if p2 <= 0:
                    raise ValueError(
                        f"Normal standard deviation must be positive: "
                        f"{patient_class}/{feature}"
                    )

                cdf = lambda x: norm.cdf(x, loc=p1, scale=p2)

            elif distribution == "lognormal":
                if p2 <= 0:
                    raise ValueError(
                        f"Lognormal sigma must be positive: "
                        f"{patient_class}/{feature}"
                    )

                cdf = lambda x: lognorm.cdf(
                    x, s=p2, loc=0, scale=np.exp(p1)
                )

            else:
                continue

            statistic, p_value = kstest(values, cdf)

            results.append({
                "class": patient_class,
                "feature": feature,
                "distribution": distribution,
                "sample_size": len(values),
                "ks_statistic": statistic,
                "p_value": p_value,
                "pass_at_0_05": p_value >= ALPHA,
            })

    result = pd.DataFrame(results)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_FILE, index=False)

    print("KS-TEST STATISTICAL VALIDATION")
    print("=" * 55)

    if result.empty:
        print("No supported numerical distribution tests were performed.")
        return

    print(result.round(4).to_string(index=False))

    passed = int(result["pass_at_0_05"].sum())
    failed = len(result) - passed

    print("\nSummary:")
    print(f"Tests performed: {len(result)}")
    print(f"Passes at alpha={ALPHA}: {passed}")
    print(f"Failures at alpha={ALPHA}: {failed}")
    print(f"Results saved to: {OUTPUT_FILE}")

    print(
        "\nInterpretation: a pass means the test did not find sufficient "
        "evidence against the specified distribution at this significance "
        "level. It does not prove that the distribution is correct."
    )


if __name__ == "__main__":
    run_ks_validation()
