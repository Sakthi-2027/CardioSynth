
from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# CARDIOSYNTH | SYNTHETIC CARDIOVASCULAR DATA DASHBOARD
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "processed"
PLOTS_DIR = BASE_DIR / "outputs" / "plots"
REPORTS_DIR = BASE_DIR / "outputs" / "reports"

PATIENT_FILE = DATA_DIR / "synthetic_patients.csv"
WAVEFORM_FILE = DATA_DIR / "patient_waveforms.csv"
SMOTE_FILE = DATA_DIR / "smote_experiment.csv"

KS_FILE = REPORTS_DIR / "ks_validation.csv"
CORRELATION_FILE = REPORTS_DIR / "correlation_validation.csv"
SUMMARY_FILE = REPORTS_DIR / "project_summary.txt"

st.set_page_config(
    page_title="CardioSynth | Analytics",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DESIGN SYSTEM
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f7fb;
        color: #172033;
    }

    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5eaf2;
    }

    [data-testid="stSidebar"] h1 {
        color: #174c77;
        font-size: 1.45rem;
    }

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2.5rem;
        max-width: 1500px;
    }

    h1, h2, h3 {
        color: #17365d;
        letter-spacing: -0.4px;
    }

    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.035);
    }

    [data-testid="stMetricLabel"] {
        color: #64748b;
        font-size: 0.9rem;
    }

    [data-testid="stMetricValue"] {
        color: #174c77;
        font-weight: 700;
    }

    .hero {
        background: linear-gradient(115deg, #ffffff, #eaf3ff);
        border: 1px solid #dbeafe;
        padding: 26px 30px;
        border-radius: 16px;
        margin-bottom: 18px;
    }

    .hero-title {
        font-size: 2rem;
        font-weight: 750;
        color: #17365d;
        margin-bottom: 5px;
    }

    .hero-subtitle {
        color: #52657d;
        font-size: 1rem;
        line-height: 1.6;
    }

    .section-note {
        color: #64748b;
        font-size: 0.9rem;
    }

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    div.stDownloadButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATA ACCESS
# ============================================================

@st.cache_data(show_spinner=False)
def load_csv(path_string: str) -> pd.DataFrame:
    """Load an existing CSV without modifying the source file."""
    path = Path(path_string)
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_text(path_string: str) -> str:
    """Read a text report if available."""
    path = Path(path_string)
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


patients = load_csv(str(PATIENT_FILE))
waveforms = load_csv(str(WAVEFORM_FILE))
ks_results = load_csv(str(KS_FILE))
correlation_results = load_csv(str(CORRELATION_FILE))
smote_data = load_csv(str(SMOTE_FILE))
project_summary = load_text(str(SUMMARY_FILE))


# ============================================================
# SHARED HELPERS
# ============================================================

def show_missing_file(path: Path, description: str) -> None:
    st.warning(f"{description} is not available yet.")
    st.caption(f"Expected file: {path.relative_to(BASE_DIR)}")
    st.code("python main.py", language="powershell")
    st.caption(
        "Run the existing pipeline from the project root to regenerate "
        "the standard datasets, charts, and reports."
    )


def find_column(
    frame: pd.DataFrame,
    candidates: list[str],
) -> str | None:
    """Find a column by case-insensitive exact name."""
    lookup = {str(col).strip().lower(): col for col in frame.columns}
    for candidate in candidates:
        if candidate.lower() in lookup:
            return lookup[candidate.lower()]
    return None


def show_image(filename: str, caption: str) -> None:
    image_path = PLOTS_DIR / filename
    if image_path.exists():
        st.image(str(image_path), caption=caption, use_container_width=True)
    else:
        st.info(f"Chart not found: outputs/plots/{filename}")


def page_heading(title: str, subtitle: str) -> None:
    st.title(title)
    st.caption(subtitle)
    st.divider()


def class_column(frame: pd.DataFrame) -> str | None:
    return find_column(
        frame,
        ["patient_class", "class", "diagnosis", "target"],
    )


def patient_id_column(frame: pd.DataFrame) -> str | None:
    return find_column(
        frame,
        ["patient_id", "id", "record_id"],
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("# 🫀 CardioSynth")
    st.caption("Synthetic Data Analytics Platform")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Overview",
            "Dataset Explorer",
            "Statistical Validation",
            "Waveform Explorer",
            "SMOTENC Experiment",
            "Project Information",
        ],
        label_visibility="visible",
    )

    st.divider()

    if not patients.empty:
        st.success("Patient dataset loaded")
    else:
        st.warning("Patient dataset unavailable")

    st.caption("Local research prototype")
    st.caption("Version 1.0")


# ============================================================
# PAGE 1 — OVERVIEW
# ============================================================

if page == "Overview":
    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">CardioSynth Analytics</div>
            <div class="hero-subtitle">
                Generate, explore, and statistically evaluate a synthetic
                multi-class cardiovascular dataset. Review dataset
                composition, numerical patterns, validation outputs,
                and mathematical pressure waveforms in one workspace.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        "Research and educational prototype only. The records are synthetic; "
        "the configured parameters and mathematical waveforms are not "
        "clinically validated and must not be used for medical decisions."
    )

    if patients.empty:
        show_missing_file(PATIENT_FILE, "Synthetic patient dataset")
    else:
        class_col = class_column(patients)
        id_col = patient_id_column(patients)

        total_patients = len(patients)
        total_classes = (
            patients[class_col].nunique()
            if class_col
            else 0
        )
        feature_count = len(
            [
                col for col in patients.columns
                if col not in {class_col, id_col}
            ]
        )
        waveform_count = len(waveforms) if not waveforms.empty else 0

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Synthetic Records", f"{total_patients:,}")
        c2.metric("Patient Classes", f"{total_classes:,}")
        c3.metric("Patient Features", f"{feature_count:,}")
        c4.metric("Waveform Points", f"{waveform_count:,}")

        st.subheader("Dataset Composition")

        left, right = st.columns([1, 1])

        with left:
            st.markdown("#### Patient Class Distribution")
            if class_col:
                counts = (
                    patients[class_col]
                    .fillna("Missing")
                    .value_counts()
                    .rename_axis("Patient Class")
                    .to_frame("Records")
                )
                st.bar_chart(counts)
                st.dataframe(counts, use_container_width=True)
            else:
                st.warning("Could not identify the patient-class column.")

        with right:
            st.markdown("#### Dataset Snapshot")
            numeric = patients.select_dtypes(include="number")
            if not numeric.empty:
                st.dataframe(
                    numeric.describe().T.round(2),
                    use_container_width=True,
                )
            else:
                st.info("No numerical columns were found.")

        st.subheader("Existing Project Visualizations")

        chart1, chart2 = st.columns(2)
        with chart1:
            show_image(
                "blood_pressure_by_class.png",
                "Blood pressure comparison by class",
            )
        with chart2:
            show_image(
                "age_distribution.png",
                "Age distribution",
            )

        chart3, chart4 = st.columns(2)
        with chart3:
            show_image(
                "correlation_heatmap.png",
                "Feature correlation heatmap",
            )
        with chart4:
            show_image(
                "class_distribution.png",
                "Patient class counts",
            )

        st.subheader("Recent Record Preview")
        st.dataframe(patients.head(10), use_container_width=True)


# ============================================================
# PAGE 2 — DATASET EXPLORER
# ============================================================

elif page == "Dataset Explorer":
    page_heading(
        "Dataset Explorer",
        "Filter records, inspect features, and export a selected subset.",
    )

    if patients.empty:
        show_missing_file(PATIENT_FILE, "Synthetic patient dataset")
    else:
        data = patients.copy()
        class_col = class_column(data)

        with st.container(border=True):
            st.markdown("#### Record Filters")

            if class_col:
                classes = sorted(
                    data[class_col].dropna().astype(str).unique().tolist()
                )
                selected_classes = st.multiselect(
                    "Patient class",
                    options=classes,
                    default=classes,
                )
                data = data[
                    data[class_col].astype(str).isin(selected_classes)
                ]

            numeric_cols = data.select_dtypes(include="number").columns.tolist()

            if numeric_cols:
                selected_features = st.multiselect(
                    "Numerical features to display",
                    options=numeric_cols,
                    default=numeric_cols,
                )
            else:
                selected_features = []

            search_text = st.text_input(
                "Search records",
                placeholder="Enter a value to search across displayed columns",
            )

        if search_text.strip():
            search_columns = selected_features + (
                [class_col] if class_col else []
            )
            search_columns = list(dict.fromkeys(
                col for col in search_columns if col in data.columns
            ))

            if search_columns:
                matches = data[search_columns].astype(str).apply(
                    lambda col: col.str.contains(
                        search_text,
                        case=False,
                        na=False,
                        regex=False,
                    )
                ).any(axis=1)
                data = data[matches]

        m1, m2, m3 = st.columns(3)
        m1.metric("Filtered Records", f"{len(data):,}")
        m2.metric("Displayed Features", len(selected_features))
        m3.metric(
            "Classes in View",
            data[class_col].nunique() if class_col and not data.empty else 0,
        )

        display_columns = list(data.columns)
        if selected_features:
            display_columns = [
                col for col in display_columns
                if col not in numeric_cols or col in selected_features
            ]

        st.subheader("Patient Records")
        st.dataframe(
            data[display_columns],
            use_container_width=True,
            height=400,
        )

        st.download_button(
            "Download filtered records (CSV)",
            data=data.to_csv(index=False).encode("utf-8"),
            file_name="cardiosynth_filtered_patients.csv",
            mime="text/csv",
        )

        st.divider()
        st.subheader("Feature Analysis")

        available_numeric = data.select_dtypes(include="number").columns.tolist()

        if available_numeric and not data.empty:
            selected_feature = st.selectbox(
                "Choose a numerical feature",
                available_numeric,
            )

            left, right = st.columns([1.4, 1])

            with left:
                st.markdown(f"#### Distribution: `{selected_feature}`")
                values = pd.to_numeric(
                    data[selected_feature],
                    errors="coerce",
                ).dropna()

                if not values.empty:
                    histogram = values.value_counts().sort_index()
                    st.bar_chart(histogram)
                else:
                    st.info("No numeric values available for this feature.")

            with right:
                st.markdown("#### Descriptive Statistics")
                if not values.empty:
                    stats = values.describe().to_frame("Value").round(3)
                    st.dataframe(stats, use_container_width=True)

            if class_col and selected_feature in data.columns:
                st.markdown("#### Feature Comparison by Class")
                grouped = data.groupby(class_col)[selected_feature].agg(
                    ["mean", "median", "std", "min", "max"]
                )
                st.dataframe(grouped.round(3), use_container_width=True)
        else:
            st.info("No records or numerical features match these filters.")


# ============================================================
# PAGE 3 — STATISTICAL VALIDATION
# ============================================================

elif page == "Statistical Validation":
    page_heading(
        "Statistical Validation",
        "Inspect the existing distribution-test and correlation reports.",
    )

    if not ks_results.empty:
        st.subheader("Kolmogorov–Smirnov (KS) Test Results")

        st.caption(
            "These tests compare generated samples with configured reference "
            "distributions. A non-rejected result does not prove that a "
            "distribution is correct or clinically representative."
        )

        st.dataframe(ks_results, use_container_width=True)

        p_col = find_column(
            ks_results,
            ["p_value", "p-value", "pvalue", "p value"],
        )
        result_col = find_column(
            ks_results,
            ["result", "status", "passed", "interpretation", "decision"],
        )

        if p_col:
            p_values = pd.to_numeric(ks_results[p_col], errors="coerce")
            valid = p_values.dropna()
            if not valid.empty:
                alpha = 0.05
                rejected = int((valid < alpha).sum())
                not_rejected = int((valid >= alpha).sum())

                a, b, c = st.columns(3)
                a.metric("Tests with Valid p-values", len(valid))
                b.metric("Not Rejected (p ≥ 0.05)", not_rejected)
                c.metric("Rejected (p < 0.05)", rejected)

        elif result_col:
            st.caption(f"Detected result column: {result_col}")

        st.download_button(
            "Download KS report",
            data=ks_results.to_csv(index=False).encode("utf-8"),
            file_name="cardiosynth_ks_validation.csv",
            mime="text/csv",
        )
    else:
        show_missing_file(KS_FILE, "KS validation report")

    st.divider()

    if not correlation_results.empty:
        st.subheader("Correlation Validation")
        st.caption(
            "The report summarizes checks on relationships among numerical "
            "features and the configured correlation structure."
        )
        st.dataframe(correlation_results, use_container_width=True)

        st.download_button(
            "Download correlation report",
            data=correlation_results.to_csv(index=False).encode("utf-8"),
            file_name="cardiosynth_correlation_validation.csv",
            mime="text/csv",
        )
    else:
        show_missing_file(
            CORRELATION_FILE,
            "Correlation validation report",
        )

    st.divider()
    st.subheader("Validation Diagnostics")
    show_image(
        "ks_failure_diagnostics.png",
        "Diagnostic visualization of KS tests that were rejected",
    )
    show_image(
        "correlation_heatmap.png",
        "Correlation heatmap of generated patient features",
    )


# ============================================================
# PAGE 4 — WAVEFORM EXPLORER
# ============================================================

elif page == "Waveform Explorer":
    page_heading(
        "Waveform Explorer",
        "Inspect mathematically generated pressure-waveform samples.",
    )

    st.info(
        "These are mathematical demonstrations generated by the project. "
        "They are not measured patient signals or validated physiological "
        "simulations."
    )

    if waveforms.empty:
        show_missing_file(WAVEFORM_FILE, "Patient waveform dataset")
    else:
        id_col = patient_id_column(waveforms)
        numeric_cols = waveforms.select_dtypes(include="number").columns.tolist()

        st.metric("Total Waveform Points", f"{len(waveforms):,}")

        if id_col:
            st.metric(
                "Patients with Waveforms",
                f"{waveforms[id_col].nunique():,}",
            )

            selected_id = st.selectbox(
                "Select patient waveform",
                sorted(waveforms[id_col].dropna().unique().tolist()),
            )
            selected = waveforms[waveforms[id_col] == selected_id]
        else:
            st.warning(
                "Patient ID column was not identified. Showing a sample "
                "of the waveform dataset instead."
            )
            selected = waveforms.head(50)

        st.subheader("Waveform Data Preview")
        st.dataframe(selected, use_container_width=True)

        pressure_col = find_column(
            selected,
            [
                "pressure",
                "pressure_value",
                "systolic_pressure",
                "blood_pressure",
                "value",
            ],
        )
        point_col = find_column(
            selected,
            [
                "point",
                "point_index",
                "time",
                "time_step",
                "sample",
                "sample_index",
            ],
        )

        if pressure_col:
            st.subheader("Pressure Signal")

            if point_col:
                plot_data = selected[[point_col, pressure_col]].copy()
                plot_data[pressure_col] = pd.to_numeric(
                    plot_data[pressure_col],
                    errors="coerce",
                )
                plot_data = plot_data.dropna().set_index(point_col)
                st.line_chart(plot_data)
            else:
                pressure_values = pd.to_numeric(
                    selected[pressure_col],
                    errors="coerce",
                ).dropna()
                st.line_chart(pressure_values.reset_index(drop=True))

            pressure_values = pd.to_numeric(
                selected[pressure_col],
                errors="coerce",
            ).dropna()

            if not pressure_values.empty:
                a, b, c = st.columns(3)
                a.metric("Minimum", f"{pressure_values.min():.2f}")
                b.metric("Maximum", f"{pressure_values.max():.2f}")
                c.metric("Mean", f"{pressure_values.mean():.2f}")
        else:
            st.warning(
                "Could not automatically identify the pressure column. "
                "Inspect the table above to see the actual column names."
            )

        st.subheader("Existing Waveform Visualization")
        show_image(
            "sample_pressure_waveforms.png",
            "Sample mathematical pressure waveforms",
        )


# ============================================================
# PAGE 5 — SMOTENC EXPERIMENT
# ============================================================

elif page == "SMOTENC Experiment":
    page_heading(
        "SMOTENC Balancing Experiment",
        "Compare the experimental balanced dataset with the original data.",
    )

    st.warning(
        "SMOTENC generates interpolated synthetic samples. This experiment "
        "does not establish clinical validity and is separate from the main "
        "generation pipeline."
    )

    if patients.empty:
        show_missing_file(PATIENT_FILE, "Original patient dataset")
    else:
        class_col = class_column(patients)

        if class_col:
            original_counts = (
                patients[class_col]
                .value_counts()
                .rename("Original Records")
            )
        else:
            original_counts = pd.Series(dtype="int64")

        if not smote_data.empty:
            smote_class_col = class_column(smote_data)

            if smote_class_col:
                balanced_counts = (
                    smote_data[smote_class_col]
                    .value_counts()
                    .rename("SMOTENC Records")
                )

                comparison = pd.concat(
                    [original_counts, balanced_counts],
                    axis=1,
                ).fillna(0).astype(int)

                st.subheader("Class Count Comparison")
                st.bar_chart(comparison)

                st.dataframe(comparison, use_container_width=True)

                st.metric(
                    "Experimental Records",
                    f"{len(smote_data):,}",
                )

                st.subheader("Experimental Dataset Preview")
                st.dataframe(
                    smote_data.head(20),
                    use_container_width=True,
                )

                st.download_button(
                    "Download SMOTENC dataset",
                    data=smote_data.to_csv(index=False).encode("utf-8"),
                    file_name="cardiosynth_smote_experiment.csv",
                    mime="text/csv",
                )
            else:
                st.warning(
                    "Could not identify the class column in the SMOTENC file."
                )
        else:
            st.info(
                "The SMOTENC experiment file was not found. "
                "Run the separate experiment when you want to generate it."
            )
            st.code("python -m src.balancing.smote_balancing")

        st.subheader("Existing SMOTENC Visualization")
        show_image(
            "smote_before_after.png",
            "Class distribution before and after SMOTENC balancing",
        )


# ============================================================
# PAGE 6 — PROJECT INFORMATION
# ============================================================

elif page == "Project Information":
    page_heading(
        "Project Information",
        "Architecture, data provenance, limitations, and project summary.",
    )

    st.subheader("Project Scope")

    st.markdown(
        """
        **CardioSynth** is an educational software prototype for generating
        and statistically inspecting synthetic multi-class cardiovascular
        records.

        **Core components**
        - Probability-distribution-based feature generation
        - Gaussian Copula-based numerical feature dependencies
        - Synthetic patient record generation
        - Dataset quality and correlation checks
        - Kolmogorov–Smirnov distribution tests
        - Mathematical pressure-waveform generation
        - A separate SMOTENC class-balancing experiment
        - Visualization and report generation
        """
    )

    st.subheader("Data Provenance and Limitations")

    limitations = [
        "The generated patient records are synthetic, not real patient data.",
        "Reference parameters are illustrative estimates, not clinical ground truth.",
        "Configured correlations are assumptions and are not clinically validated.",
        "Mathematical pressure waveforms are demonstrations, not measured signals.",
        "Statistical test results assess configured generation behavior, not medical accuracy.",
        "The dashboard is not a diagnostic or treatment tool.",
    ]

    for limitation in limitations:
        st.markdown(f"- {limitation}")

    st.divider()
    st.subheader("Generated Project Summary")

    if project_summary:
        st.code(project_summary, language="text")
    else:
        show_missing_file(SUMMARY_FILE, "Project summary report")

    st.subheader("Project Paths")
    st.code(
        f"Project root: {BASE_DIR}\n"
        f"Patient dataset: {PATIENT_FILE}\n"
        f"Waveform dataset: {WAVEFORM_FILE}\n"
        f"Charts: {PLOTS_DIR}\n"
        f"Reports: {REPORTS_DIR}",
        language="text",
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()
st.caption(
    "CardioSynth | Synthetic data research prototype | "
    "Statistical consistency does not establish clinical validity."
)
