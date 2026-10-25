
@'
# CardioSynth — Synthetic Cardiovascular Dataset Generation and Statistical Validation

CardioSynth is a Python-based project that generates synthetic cardiovascular-style patient data and evaluates its statistical properties through data-quality checks, distribution tests, correlation analysis, and mathematical pressure waveform validation.

> **Disclaimer:** This project is for educational and software prototyping purposes only. It does not generate real patient records, provide medical diagnoses, or establish clinical validity.

## Project Objectives

- Generate a reproducible synthetic dataset with four patient categories.
- Model selected numerical dependencies using a Gaussian Copula.
- Generate illustrative numerical, binary, and categorical features.
- Create mathematical pressure waveform samples.
- Validate dataset quality, feature distributions, correlations, and waveform structure.
- Produce reports and visualizations for analysis.

## Dataset Overview

| Property | Description |
|---|---|
| Patient records | 2,000 |
| Patient categories | 4 |
| Records per category | 500 |
| Features per patient | 12 |
| Waveform points per patient | 50 |
| Total waveform points | 100,000 |

### Patient Categories

- Normal
- Hypertension
- Arrhythmia
- Valve Disorder

### Features

Age, sex, systolic blood pressure, diastolic blood pressure, heart rate, maximum heart rate, cholesterol, fasting blood sugar, exercise-induced angina, ST depression, chest pain type, and major vessels.

## Methodology

### 1. Synthetic Data Generation
Class-specific parameters define illustrative normal, Bernoulli, lognormal, and categorical distributions.

### 2. Gaussian Copula
A Gaussian Copula introduces assumed dependencies between selected numerical features. These relationships are design assumptions, not clinically validated correlations.

### 3. Pressure Waveform Generation
The project generates 50-point mathematical pressure waveforms using systolic and diastolic blood pressure values. These are demonstrations, not measured physiological signals.

### 4. Validation
The pipeline includes:
- Missing-value, uniqueness, class-balance, and range checks.
- Kolmogorov–Smirnov (KS) distribution tests.
- Correlation matrix analysis.
- Waveform structure and range checks.
- Summary reports and diagnostic plots.

## Current Validation Results

- 2,000 patient records generated.
- 500 records in each of the four categories.
- All mandatory patient data-quality checks passed.
- 100,000 waveform points generated and passed the configured structural checks.
- 28 KS tests performed: 24 did not reject their configured target distributions at the 0.05 significance level, while 4 rejected them.

A non-rejected KS test does not prove that a distribution is correct. Results may be affected by clipping, rounding, constraints, sampling variability, and multiple testing.

## Technology Stack

- Python
- NumPy
- pandas
- SciPy
- Matplotlib
- Seaborn

## Project Structure

```text
CardioSynth/
├── config/
├── data/
│   ├── raw/
│   └── processed/
├── docs/
├── notebooks/
├── outputs/
│   ├── plots/
│   └── reports/
├── src/
│   ├── generation/
│   ├── validation/
│   ├── waveform/
│   └── balancing/
├── tests/
├── inspect_failures.py
├── main.py
├── requirements.txt
├── README.md
└── REPORT.md
```

## Setup

### Prerequisites
- Python 3.10 or later
- pip

### Install dependencies

```bash
python -m venv venv
```

Activate the environment on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

### Run individual modules

Run commands from the project root after activating the virtual environment.

Generate dataset visualizations:

```bash
python -m src.validation.visualize_dataset
```

Run correlation validation:

```bash
python -m src.validation.correlation_validation
```

Run distribution validation:

```bash
python -m src.validation.ks_validation
```

Generate the project summary:

```bash
python -m src.validation.project_report
```

Generate and validate waveforms using the relevant modules under `src/waveform/`.

**Note:** These are individual module commands. The root-level `main.py` pipeline is not yet configured.

## Limitations

- Reference parameters are illustrative estimates, not clinical ground truth.
- Copula dependencies are assumed and have not been clinically validated.
- Generated pressure waveforms are mathematical demonstrations, not measured physiological signals.
- Statistical consistency with configured parameters does not establish real-world clinical validity.
- The dataset should not be used for diagnosis, treatment, or clinical decision-making.

## Future Enhancements

- Build a unified pipeline through `main.py`.
- Add automated unit and integration tests.
- Improve distribution-fit diagnostics and account for multiple comparisons.
- Add reproducibility and configuration options.
- Document and test optional class-balancing functionality.
- Add a clearly labeled sample dataset and representative visualizations.

## Project Report

See [REPORT.md](REPORT.md) for the detailed methodology, validation results, limitations, and project findings.

---

**CardioSynth** — Synthetic data generation and statistical validation for educational research.
'@ | Set-Content -Encoding utf8 README.md
