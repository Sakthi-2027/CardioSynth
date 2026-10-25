
from src.generation.synthetic_patients import generate_patients, save_patients
from src.waveform.pressure_waveform import save_all_patient_waveforms

from src.validation.validation_report import validate_dataset
from src.validation.correlation_validation import validate_correlations
from src.validation.ks_validation import run_ks_validation
from src.validation.visualize_dataset import create_visualizations
from src.waveform.validate_waveforms import validate_waveforms
from src.waveform.visualize_waveforms import visualize_waveforms
from src.validation.project_report import generate_project_report


def main():
    print("\n" + "=" * 60)
    print("CARDIOSYNTH — COMPLETE PROJECT PIPELINE")
    print("=" * 60)

    print("\n[1/9] Generating synthetic patients...")
    patients = generate_patients()
    save_patients(patients)

    print("\n[2/9] Generating patient waveforms...")
    save_all_patient_waveforms()

    print("\n[3/9] Validating patient dataset...")
    data, issues = validate_dataset()

    if issues:
        print("\nData-quality validation failed:")
        for issue in issues:
            print(f"- {issue}")
        raise SystemExit("Pipeline stopped because of data-quality issues.")

    print("\n[4/9] Validating correlations...")
    validate_correlations(data)

    print("\n[5/9] Running KS distribution tests...")
    run_ks_validation()

    print("\n[6/9] Creating dataset visualizations...")
    create_visualizations()

    print("\n[7/9] Validating waveforms...")
    validate_waveforms()

    print("\n[8/9] Creating waveform visualizations...")
    visualize_waveforms()

    print("\n[9/9] Generating project summary...")
    generate_project_report()

    print("\n" + "=" * 60)
    print("CARDIOSYNTH PIPELINE FINISHED")
    print("=" * 60)
    print("Check the outputs/ folder for plots and reports.")
    print("Note: statistical consistency does not establish clinical validity.")


if __name__ == "__main__":
    main()
