
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

reference = pd.read_csv("data/raw/reference_values.csv")
data = pd.read_csv("data/processed/synthetic_patients.csv")

failed_features = [
    ("Arrhythmia", "max_heart_rate"),
    ("Normal", "cholesterol"),
    ("Valve Disorder", "age"),
    ("Valve Disorder", "max_heart_rate"),
]

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

for ax, (patient_class, feature) in zip(
    axes.flatten(), failed_features
):
    ref = reference[
        (reference["class"] == patient_class)
        & (reference["feature"] == feature)
    ].iloc[0]

    values = data.loc[
        data["class"] == patient_class, feature
    ].dropna().to_numpy()

    mean = float(ref["parameter_1"])
    sd = float(ref["parameter_2"])

    ax.hist(
        values, bins=25, density=True, alpha=0.7,
        label="Generated data"
    )

    x = np.linspace(values.min(), values.max(), 300)
    ax.plot(
        x, norm.pdf(x, loc=mean, scale=sd),
        linewidth=2, label="Target normal distribution"
    )

    ax.set_title(f"{patient_class}: {feature}")
    ax.set_xlabel(feature)
    ax.set_ylabel("Density")
    ax.legend()

plt.tight_layout()
plt.savefig(
    "outputs/plots/ks_failure_diagnostics.png",
    dpi=150
)
plt.show()

print("Saved: outputs/plots/ks_failure_diagnostics.png")
