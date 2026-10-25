
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from config.settings import DATA_FILE, PLOT_DIR


def create_visualizations():
    data = pd.read_csv(DATA_FILE)

    sns.set_theme(style="whitegrid")
    PLOT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Class distribution
    plt.figure(figsize=(8, 5))
    order = [
        "Normal",
        "Hypertension",
        "Arrhythmia",
        "Valve Disorder",
    ]

    sns.countplot(data=data, x="class", order=order)
    plt.title("CardioSynth: Patient Class Distribution")
    plt.xlabel("Patient Class")
    plt.ylabel("Number of Synthetic Patients")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "class_distribution.png", dpi=200)
    plt.close()

    # 2. Systolic blood pressure by class
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=data, x="class", y="systolic_bp", order=order)
    plt.title("Systolic Blood Pressure by Patient Class")
    plt.xlabel("Patient Class")
    plt.ylabel("Systolic BP (mmHg)")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "blood_pressure_by_class.png", dpi=200)
    plt.close()

    # 3. Age distribution
    plt.figure(figsize=(8, 5))
    sns.histplot(
        data=data,
        x="age",
        hue="class",
        bins=25,
        element="step",
        stat="density",
        common_norm=False,
    )
    plt.title("Age Distribution Across Synthetic Patient Classes")
    plt.xlabel("Age (years)")
    plt.ylabel("Density")
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "age_distribution.png", dpi=200)
    plt.close()

    # 4. Correlation heatmap
    numerical_features = [
        "age",
        "systolic_bp",
        "diastolic_bp",
        "heart_rate",
        "max_heart_rate",
        "cholesterol",
        "st_depression",
    ]

    plt.figure(figsize=(9, 7))
    correlation = data[numerical_features].corr()
    sns.heatmap(
        correlation,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
    )
    plt.title("Feature Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "correlation_heatmap.png", dpi=200)
    plt.close()

    print("Visualizations generated successfully!")

    for filename in [
        "class_distribution.png",
        "blood_pressure_by_class.png",
        "age_distribution.png",
        "correlation_heatmap.png",
    ]:
        print(PLOT_DIR / filename)


if __name__ == "__main__":
    create_visualizations()
