
import numpy as np


def sample_feature(distribution, parameter_1, parameter_2=None, rng=None):
    """Generate one value from a configured probability distribution."""
    if rng is None:
        rng = np.random.default_rng()

    if distribution == "normal":
        mean = float(parameter_1)
        std = float(parameter_2)

        if std <= 0:
            raise ValueError("Normal distribution standard deviation must be positive.")

        return float(rng.normal(mean, std))

    elif distribution == "bernoulli":
        probability = float(parameter_1)

        if not 0 <= probability <= 1:
            raise ValueError("Bernoulli probability must be between 0 and 1.")

        return int(rng.binomial(1, probability))

    elif distribution == "lognormal":
        # Here parameter_1 is the underlying normal mean (mu),
        # and parameter_2 is its standard deviation (sigma).
        mu = float(parameter_1)
        sigma = float(parameter_2)

        if sigma <= 0:
            raise ValueError("Lognormal sigma must be positive.")

        return float(rng.lognormal(mu, sigma))

    elif distribution == "categorical":
        probabilities = np.array(
            [float(x) for x in str(parameter_1).split(";")],
            dtype=float,
        )

        if np.any(probabilities < 0) or not np.isclose(probabilities.sum(), 1.0):
            raise ValueError("Categorical probabilities must sum to 1.")

        categories = np.arange(len(probabilities))
        return int(rng.choice(categories, p=probabilities))

    else:
        raise ValueError(f"Unsupported distribution: {distribution}")


if __name__ == "__main__":
    rng = np.random.default_rng(42)

    print("Normal — age:", round(sample_feature("normal", 58, 12, rng)))
    print("Bernoulli — sex:", sample_feature("bernoulli", 0.5, rng=rng))
    print("Lognormal — ST depression:", round(sample_feature("lognormal", 0.2, 0.4, rng), 2))
    print("Categorical — chest pain:", sample_feature("categorical", "0.7;0.1;0.1;0.1", rng=rng))
