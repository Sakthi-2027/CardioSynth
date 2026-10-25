
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = PROJECT_ROOT / "data" / "processed" / "synthetic_patients.csv"
PLOT_DIR = PROJECT_ROOT / "outputs" / "plots"

PLOT_DIR.mkdir(parents=True, exist_ok=True)
