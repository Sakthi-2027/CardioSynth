# CardioSynth — Synthetic Multi-Class Cardiovascular Patient Database Generation and Statistical Validation

## 1. Abstract

CardioSynth is a Python-based project for generating and statistically validating a synthetic cardiovascular patient database. The system generates 2,000 synthetic patient records distributed equally across four cardiovascular-related classes: Normal, Hypertension, Arrhythmia, and Valve Disorder.

The generated dataset contains 12 patient features including demographic, physiological, laboratory, and cardiovascular-related variables. A Gaussian Copula-based approach is used to introduce assumed dependencies between selected numerical variables while class-specific probability distributions are used to generate individual features.

In addition to tabular patient data, CardioSynth generates mathematical pressure waveforms using systolic and diastolic blood pressure values. The generated data is evaluated using data-quality checks, Kolmogorov-Smirnov (KS) distribution tests, correlation analysis, and waveform validation.

The project is intended for educational and software-development purposes. The generated data is synthetic and illustrative and must not be interpreted as real patient data or clinically validated medical information.

## 2. Problem Statement

Obtaining large cardiovascular datasets can be difficult because real patient data may involve privacy restrictions, limited availability, and complex data-access requirements.

CardioSynth addresses this software and research-prototyping problem by providing a reproducible method for generating synthetic cardiovascular-style patient records from predefined statistical parameters.

The goal is not to reproduce real patient populations exactly, but to demonstrate how statistical distributions, dependency modeling, synthetic data generation, and validation techniques can be combined into a complete data-generation pipeline.

## 3. Objectives

The main objectives of CardioSynth are:

1. Generate a structured synthetic cardiovascular patient dataset.
2. Maintain equal representation across four patient classes.
3. Model selected dependencies between numerical features using a Gaussian Copula.
4. Generate categorical and binary cardiovascular-related attributes.
5. Generate mathematical pressure waveforms from blood-pressure values.
6. Perform automated data-quality validation.
7. Compare generated numerical features against predefined target distributions.
8. Evaluate correlations between selected numerical variables.
9. Produce visualizations for dataset analysis.
10. Generate a reproducible project summary and validation reports.

## 4. Dataset Overview

CardioSynth generates a total of 2,000 synthetic patient records.

| Class | Records |
|---|---:|
| Normal | 500 |
| Hypertension | 500 |
| Arrhythmia | 500 |
| Valve Disorder | 500 |
| **Total** | **2,000** |

Each patient has 12 generated features:

- Age
- Sex
- Systolic Blood Pressure
- Diastolic Blood Pressure
- Heart Rate
- Maximum Heart Rate
- Cholesterol
- Fasting Blood Sugar
- Exercise-Induced Angina
- ST Depression
- Chest Pain Type
- Major Vessels

Each patient also receives a unique patient identifier and a class label.

## 5. Synthetic Data Generation Methodology

The generation pipeline uses different statistical techniques depending on the feature type.

### 5.1 Numerical Features

Numerical variables are generated using predefined probability distributions. Most numerical variables use normal distributions, while ST depression uses a lognormal distribution.

The reference parameters contain a target mean and standard deviation or corresponding distribution parameters for each class.

These parameters are illustrative assumptions used to control the synthetic generator and are not claimed to represent clinical ground truth.

### 5.2 Binary Features

Binary features such as sex, fasting blood sugar, and exercise-induced angina are generated using Bernoulli distributions.

A Bernoulli distribution produces one of two possible outcomes, represented here as 0 or 1.

### 5.3 Categorical Features

Categorical variables such as chest pain type and major vessels are generated using predefined categorical probability distributions.

This allows different categories to occur with specified probabilities rather than using a simple uniform random selection.

## 6. Gaussian Copula Dependency Modeling

Independent sampling of every feature can produce unrealistic relationships between variables. CardioSynth therefore uses a Gaussian Copula to introduce dependencies between selected numerical variables.

The project models assumed relationships such as:

- Age and systolic blood pressure
- Age and diastolic blood pressure
- Age and maximum heart rate
- Systolic and diastolic blood pressure
- Heart rate and maximum heart rate
- Age and cholesterol

The Gaussian Copula first generates correlated latent normal variables and transforms them into uniform probabilities. These probabilities are then mapped into the desired feature-specific distributions.

The correlation values used by the project are assumed dependency parameters for demonstrating the methodology. They have not been clinically validated.

## 7. Patient Data Generation Pipeline

The overall generation pipeline can be summarized as:

**Reference Parameters → Dependency Modeling → Distribution Sampling → Constraint Handling → Synthetic Patient Dataset → Validation**

During generation, basic consistency constraints are applied. For example, systolic blood pressure must exceed diastolic blood pressure, and maximum heart rate must not be lower than resting heart rate.

These constraints improve software-level consistency but can also slightly alter the original statistical distributions.

## 8. Pressure Waveform Generation

CardioSynth additionally generates a mathematical pressure waveform for every synthetic patient.

Each patient receives 50 waveform points derived from their systolic and diastolic blood-pressure values.

For 2,000 patients:

**2,000 × 50 = 100,000 waveform points**

The waveform represents a simplified pressure pattern and includes small random perturbations.

These waveforms are mathematical demonstrations for the project and should not be interpreted as measured arterial pressure signals, ECG signals, or physiologically accurate hemodynamic simulations.

## 9. Data Quality Validation

The generated patient dataset is automatically checked for:

- Expected number of records
- Unique patient identifiers
- Missing values
- Expected patient classes
- Equal class distribution
- Numerical feature ranges
- Binary feature validity
- Categorical feature validity
- Systolic blood pressure greater than diastolic blood pressure

The current generated dataset contains:

**2,000 records with 0 missing values and 500 records in each class.**

All mandatory data-quality checks passed.

## 10. Statistical Validation

CardioSynth uses statistical validation to compare generated numerical variables against their predefined target distributions.

The primary distribution test used is the **Kolmogorov-Smirnov (KS) test**.

The project performed:

**28 KS distribution tests**

Results:

- **24 tests:** did not reject the target distribution at α = 0.05
- **4 tests:** rejected the target distribution at α = 0.05

A non-rejected KS test does not prove that the generated data is clinically correct. It only indicates that there is insufficient statistical evidence, at the selected significance level, to reject the tested target distribution.

The four rejected tests are retained in the results rather than artificially modifying the generator to force every test to pass.

## 11. Correlation Validation

The project also evaluates the Pearson correlation matrix of selected numerical features.

The generated correlation matrix is checked for:

- Symmetry
- Unit diagonal
- Positive-semidefinite behavior

The generated matrix passed these structural checks.

The correlation analysis is intended to verify the behavior of the synthetic generation process and its assumed dependencies. It should not be interpreted as evidence that the modeled relationships represent real clinical relationships.

## 12. Waveform Validation

The waveform dataset contains:

- 2,000 patients
- 50 points per patient
- 100,000 total waveform points

Automated validation confirms:

- Required columns are present.
- No missing waveform values exist.
- Exactly 2,000 patients have waveforms.
- Every patient has exactly 50 waveform points.
- Pressure values remain within the configured software sanity bounds.

These checks validate dataset integrity rather than physiological accuracy.

## 13. Project Outputs

The project generates several outputs including:

- Synthetic patient dataset
- Patient waveform dataset
- KS validation results
- Correlation validation results
- Dataset visualizations
- Waveform visualizations
- KS failure diagnostic plot
- Project summary report

Important generated files include:

```text
data/processed/synthetic_patients.csv
data/processed/patient_waveforms.csv
outputs/reports/ks_validation.csv
outputs/reports/correlation_validation.csv
outputs/reports/project_summary.txt
outputs/plots/class_distribution.png
outputs/plots/blood_pressure_by_class.png
outputs/plots/age_distribution.png
outputs/plots/correlation_heatmap.png
outputs/plots/sample_pressure_waveforms.png
```

## 14. Limitations

The project has several important limitations.

1. The reference parameters are illustrative estimates rather than validated clinical reference values.
2. The Gaussian Copula dependency structure is assumed and has not been derived from a validated clinical dataset.
3. Constraint corrections can modify the generated marginal distributions.
4. KS tests evaluate statistical similarity to predefined distributions but do not establish clinical validity.
5. Multiple statistical tests require cautious interpretation of p-values.
6. The generated pressure waveforms are mathematical demonstrations rather than measured physiological signals.
7. The synthetic dataset should not be used for medical diagnosis, treatment decisions, or clinical research without appropriate validation.

## 15. Conclusion

CardioSynth demonstrates a complete synthetic data-generation and statistical-validation pipeline for a cardiovascular-style dataset.

The system successfully generates 2,000 synthetic patient records across four classes, produces 100,000 waveform points, validates dataset integrity, evaluates predefined statistical distributions, and analyzes feature correlations.

The project demonstrates practical concepts including probability distributions, Gaussian Copulas, synthetic data generation, statistical hypothesis testing, correlation analysis, data validation, visualization, and reproducible Python pipelines.

The results show that the generated dataset is internally consistent with the project's configured assumptions. However, statistical consistency with assumed parameters should not be confused with clinical validity.

## 16. Future Enhancements

Potential future improvements include:

- Learning distribution parameters from a validated real-world dataset.
- Learning the correlation matrix from real reference data.
- Applying more advanced copula models.
- Adding multivariate statistical validation.
- Adding privacy-preserving synthetic data evaluation.
- Comparing multiple synthetic-data generation techniques.
- Developing more realistic physiological waveform models.
- Adding automated experiment tracking.
- Adding a web-based dashboard for dataset exploration.
- Performing stronger external validation against independent reference datasets.

## 17. Final Project Status

**Status: Successfully implemented**

Current dataset:

- **2,000 synthetic patients**
- **4 patient classes**
- **500 patients per class**
- **12 patient features**
- **100,000 waveform points**
- **50 waveform points per patient**
- **28 KS distribution tests**
- **24 non-rejected KS tests**
- **4 rejected KS tests**
- **Data-quality validation: PASSED**
- **Waveform validation: PASSED**
- **Correlation structural validation: PASSED**

**CardioSynth is an educational synthetic-data generation and statistical-validation project and is not a clinical medical system.**

## SMOTENC Class-Balancing Experiment

### Objective
To demonstrate how a class-imbalanced synthetic cardiovascular dataset can be balanced using Synthetic Minority Over-sampling Technique for Nominal and Continuous features (SMOTENC).

### Experimental Procedure
The original CardioSynth dataset contains 2,000 synthetic records, with 500 records in each of the four classes: Normal, Hypertension, Arrhythmia, and Valve Disorder.

For this experiment, a separate imbalanced subset was created by reducing the Arrhythmia class to 100 records while retaining 500 records for each of the other classes. This produced an experimental dataset of 1,600 records.

SMOTENC was then applied to oversample the minority class. Categorical features were specified separately so that the method could handle categorical and continuous features appropriately.

### Results

| Patient class | Before SMOTENC | After SMOTENC |
|---|---:|---:|
| Arrhythmia | 100 | 500 |
| Hypertension | 500 | 500 |
| Normal | 500 | 500 |
| Valve Disorder | 500 | 500 |
| **Total** | **1,600** | **2,000** |

### Output Artifacts
- Balanced experimental dataset: `data/processed/smote_experiment.csv`
- Before-and-after class distribution chart: `outputs/plots/smote_before_after.png`
- Implementation: `src/balancing/smote_balancing.py`

### Interpretation
The experiment successfully increased the minority-class count from 100 to 500, producing equal class counts across all four categories. The original dataset was preserved separately.

### Limitations
The generated records are interpolated from an already synthetic dataset. Balanced class counts do not establish clinical validity or guarantee improved predictive performance. No classifier evaluation was performed as part of this experiment. SMOTENC balancing was executed separately from the main project pipeline.
