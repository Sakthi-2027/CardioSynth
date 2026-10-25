
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm, lognorm

from src.generation.copula import sample_gaussian_copula
from src.generation.distributions import sample_feature
from src.generation.reference_data import load_reference_data


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "synthetic_patients.csv"

PATIENTS_PER_CLASS = 500

PATIENT_CLASSES = [
    "Normal",
    "Hypertension",
    "Arrhythmia",
    "Valve Disorder",
]

NUMERICAL_FEATURES = [
    "age",
    "systolic_bp",
    "diastolic_bp",
    "heart_rate",
    "max_heart_rate",
    "cholesterol",
    "st_depression",
]

FEATURE_BOUNDS = {
    "age": (18, 100),
    "systolic_bp": (70, 250),
    "diastolic_bp": (40, 150),
    "heart_rate": (30, 220),
    "max_heart_rate": (40, 220),
    "cholesterol": (80, 500),
    "st_depression": (0, 10),
}

# Illustrative dependency assumptions, not clinically validated estimates.
# Feature order must match NUMERICAL_FEATURES.
COPULA_CORRELATION = np.eye(len(NUMERICAL_FEATURES))

def set_correlation(feature_a, feature_b, value):
    i = NUMERICAL_FEATURES.index(feature_a)
    j = NUMERICAL_FEATURES.index(feature_b)
    COPULA_CORRELATION[i, j] = value
    COPULA_CORRELATION[j, i] = value


set_correlation("age", "systolic_bp", 0.25)
set_correlation("age", "diastolic_bp", 0.20)
set_correlation("age", "max_heart_rate", -0.40)
set_correlation("systolic_bp", "diastolic_bp", 0.45)
set_correlation("heart_rate", "max_heart_rate", 0.20)
set_correlation("age", "cholesterol", 0.10)


def inverse_distribution(u, distribution, parameter_1, parameter_2):
    """Convert uniform probabilities into class-specific feature values."""
    u = np.clip(u, 1e-10, 1 - 1e-10)

    if distribution == "normal":
        mean = float(parameter_1)
        std = float(parameter_2)

        if std <= 0:
            raise ValueError("Normal distribution std must be positive.")

        return norm.ppf(u, loc=mean, scale=std)

    if distribution == "lognormal":
        mu = float(parameter_1)
        sigma = float(parameter_2)

        if sigma <= 0:
            raise ValueError("Lognormal sigma must be positive.")

        return lognorm.ppf(u, s=sigma, scale=np.exp(mu))

    raise ValueError(
        f"Copula inverse sampling does not support {distribution!r}."
    )


def generate_patients(
    patients_per_class=PATIENTS_PER_CLASS,
    random_seed=42,
):
    """Generate synthetic profiles with Copula-linked numerical features."""
    if patients_per_class < 1:
        raise ValueError("patients_per_class must be at least 1.")

    reference = load_reference_data()
    rng = np.random.default_rng(random_seed)
    records = []
    patient_number = 1

    for patient_class in PATIENT_CLASSES:
        class_reference = reference[
            reference["class"] == patient_class
        ]

        if class_reference.empty:
            raise ValueError(
                f"No reference parameters found for {patient_class}."
            )

        parameters_by_feature = {
            row["feature"]: row
            for _, row in class_reference.iterrows()
        }

        # Generate one correlated probability vector per patient.
        uniforms = sample_gaussian_copula(
            COPULA_CORRELATION,
            n_samples=patients_per_class,
            random_seed=random_seed + patient_number,
        )

        for patient_index in range(patients_per_class):
            patient = {
                "patient_id": f"SYN_{patient_number:04d}",
                "class": patient_class,
            }

            for feature, parameter in parameters_by_feature.items():
                distribution = parameter["distribution"]

                if feature in NUMERICAL_FEATURES:
                    column = NUMERICAL_FEATURES.index(feature)
                    value = inverse_distribution(
                        uniforms[patient_index, column],
                        distribution,
                        parameter["parameter_1"],
                        parameter["parameter_2"],
                    )
                else:
                    value = sample_feature(
                        distribution=distribution,
                        parameter_1=parameter["parameter_1"],
                        parameter_2=parameter["parameter_2"],
                        rng=rng,
                    )

                patient[feature] = value

            # Apply documented engineering bounds.
            for feature, (lower, upper) in FEATURE_BOUNDS.items():
                patient[feature] = float(
                    np.clip(patient[feature], lower, upper)
                )

            patient["age"] = int(round(patient["age"]))

            # Enforce systolic BP > diastolic BP by resampling SBP.
            sbp_parameter = parameters_by_feature["systolic_bp"]

            for _ in range(100):
                if patient["systolic_bp"] > patient["diastolic_bp"]:
                    break

                patient["systolic_bp"] = float(
                    np.clip(
                        sample_feature(
                            sbp_parameter["distribution"],
                            sbp_parameter["parameter_1"],
                            sbp_parameter["parameter_2"],
                            rng=rng,
                        ),
                        *FEATURE_BOUNDS["systolic_bp"],
                    )
                )
            else:
                raise ValueError(
                    f"Could not generate consistent BP for "
                    f"{patient['patient_id']}."
                )

            # Enforce maximum heart rate >= resting heart rate.
            max_hr_parameter = parameters_by_feature["max_heart_rate"]

            for _ in range(100):
                if patient["max_heart_rate"] >= patient["heart_rate"]:
                    break

                patient["max_heart_rate"] = float(
                    np.clip(
                        sample_feature(
                            max_hr_parameter["distribution"],
                            max_hr_parameter["parameter_1"],
                            max_hr_parameter["parameter_2"],
                            rng=rng,
                        ),
                        *FEATURE_BOUNDS["max_heart_rate"],
                    )
                )
            else:
                raise ValueError(
                    f"Could not generate consistent heart rates for "
                    f"{patient['patient_id']}."
                )

            records.append(patient)
            patient_number += 1

    data = pd.DataFrame(records)

    for feature in [
        "sex",
        "fasting_blood_sugar",
        "exercise_angina",
        "chest_pain_type",
        "major_vessels",
    ]:
        data[feature] = data[feature].astype(int)

    return data


def save_patients(data):
    """Save the generated dataset."""
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(OUTPUT_FILE, index=False)
    print(f"\nDataset saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    patients = generate_patients()

    print("Copula-based synthetic patient generation successful!")
    print(f"Total patients: {len(patients)}")
    print(f"Features (excluding ID and class): {len(patients.columns) - 2}")
    print("\nClass distribution:")
    print(
        patients["class"]
        .value_counts()
        .reindex(PATIENT_CLASSES, fill_value=0)
        .to_string()
    )

    print("\nNumerical feature correlations:")
    print(patients[NUMERICAL_FEATURES].corr().round(2))

    save_patients(patients)
