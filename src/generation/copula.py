import numpy as np
import pandas as pd
from scipy.stats import norm, rankdata


NUMERICAL_FEATURES = [
    "age",
    "systolic_bp",
    "diastolic_bp",
    "heart_rate",
    "max_heart_rate",
    "cholesterol",
    "st_depression",
]


def estimate_correlation(data):
    """
    Estimate a Gaussian Copula correlation matrix
    from the rank-transformed numerical features.
    """
    missing = set(NUMERICAL_FEATURES) - set(data.columns)
    if missing:
        raise ValueError(f"Missing features: {sorted(missing)}")

    values = data[NUMERICAL_FEATURES].to_numpy(dtype=float)

    if not np.isfinite(values).all():
        raise ValueError("Input contains missing or non-finite values.")

    n_samples = len(data)
    if n_samples < 3:
        raise ValueError("At least three records are required.")

    # Convert each feature to ranks and then standard normal scores.
    normal_scores = np.empty_like(values, dtype=float)

    for column in range(values.shape[1]):
        ranks = rankdata(values[:, column], method="average")
        probabilities = (ranks - 0.5) / n_samples
        normal_scores[:, column] = norm.ppf(probabilities)

    correlation = np.corrcoef(normal_scores, rowvar=False)

    # Numerical stabilization: enforce symmetry and unit diagonal.
    correlation = (correlation + correlation.T) / 2
    np.fill_diagonal(correlation, 1.0)

    return pd.DataFrame(
        correlation,
        index=NUMERICAL_FEATURES,
        columns=NUMERICAL_FEATURES,
    )


def sample_gaussian_copula(
    correlation,
    n_samples,
    random_seed=42,
):
    """
    Generate correlated uniform samples using a Gaussian Copula.

    Returns values in (0, 1), suitable for inverse-CDF sampling.
    """
    if n_samples < 1:
        raise ValueError("n_samples must be at least 1.")

    matrix = np.asarray(correlation, dtype=float)

    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("Correlation matrix must be square.")

    if not np.isfinite(matrix).all():
        raise ValueError("Correlation matrix contains non-finite values.")

    if not np.allclose(matrix, matrix.T, atol=1e-8):
        raise ValueError("Correlation matrix must be symmetric.")

    if not np.allclose(np.diag(matrix), 1.0, atol=1e-6):
        raise ValueError("Correlation matrix must have a unit diagonal.")

    eigenvalues = np.linalg.eigvalsh(matrix)
    if eigenvalues.min() < -1e-8:
        raise ValueError(
            "Correlation matrix is not positive semidefinite."
        )

    # Add a tiny diagonal adjustment if necessary for stable factorization.
    matrix = matrix + np.eye(matrix.shape[0]) * 1e-10
    scale = np.sqrt(np.diag(matrix))
    matrix = matrix / np.outer(scale, scale)

    rng = np.random.default_rng(random_seed)
    factor = np.linalg.cholesky(matrix)

    independent_normals = rng.standard_normal(
        size=(n_samples, matrix.shape[0])
    )
    correlated_normals = independent_normals @ factor.T

    # Transform correlated normal values to uniform probabilities.
    uniforms = norm.cdf(correlated_normals)

    return uniforms



if __name__ == "__main__":
    rng = np.random.default_rng(42)
    n = 500

    # Illustrative data with noisy, non-perfect relationships.
    age = np.clip(rng.normal(55, 14, n), 18, 100)

    sample_data = pd.DataFrame({
        "age": age,
        "systolic_bp": (
            120 + 0.35 * (age - 50) + rng.normal(0, 15, n)
        ),
        "diastolic_bp": (
            78 + 0.15 * (age - 50) + rng.normal(0, 9, n)
        ),
        "heart_rate": rng.normal(80, 15, n),
        "max_heart_rate": (
            190 - 0.7 * age + rng.normal(0, 15, n)
        ),
        "cholesterol": (
            190 + 0.25 * (age - 50) + rng.normal(0, 30, n)
        ),
        "st_depression": rng.lognormal(mean=0.2, sigma=0.5, size=n),
    })

    correlation = estimate_correlation(sample_data)

    print("Estimated Gaussian Copula correlation matrix:")
    print(correlation.round(2))

    uniforms = sample_gaussian_copula(
        correlation.to_numpy(),
        n_samples=5,
        random_seed=42,
    )

    print("\nFive correlated uniform samples:")
    print(np.round(uniforms, 3))

    print("\nAll generated values are strictly between 0 and 1:",
          bool(np.all((uniforms > 0) & (uniforms < 1))))
