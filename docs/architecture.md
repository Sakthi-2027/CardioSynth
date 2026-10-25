
# CardioSynth — System Architecture

```mermaid
flowchart TD
    A["Reference Parameters<br/>reference_values.csv"]
    B["Distribution Sampling<br/>Normal, Bernoulli, Lognormal, Categorical"]
    C["Gaussian Copula<br/>Model assumed feature dependencies"]
    D["Synthetic Patient Generation"]
    E[("synthetic_patients.csv<br/>2,000 records · 4 classes · 12 features")]

    F["Data Quality Validation"]
    G["Correlation Validation"]
    H["KS Distribution Tests"]

    I["Mathematical Pressure Waveform Generation"]
    J[("patient_waveforms.csv<br/>100,000 waveform points")]

    K["Dataset Visualizations"]
    L["Waveform Validation and Visualization"]
    M["Project Summary and Validation Reports"]

    N["Separate SMOTENC Experiment"]
    O[("smote_experiment.csv<br/>2,000 experimental records")]

    A --> B
    A --> C
    B --> D
    C --> D
    D --> E

    E --> F
    E --> G
    E --> H
    E --> I
    I --> J

    F --> K
    G --> M
    H --> M
    J --> L
    L --> M
    K --> M

    E -. "Separate experimental subset" .-> N
    N --> O
```

## Important Notes

- Gaussian Copula models **assumed statistical dependencies**; these are not clinically validated relationships.
- The pressure waveforms are mathematical demonstrations, not measured patient signals.
- SMOTENC runs separately and does not modify the original patient dataset.
- The architecture represents the implemented project workflow, not a clinical diagnostic system.
