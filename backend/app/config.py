from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SALES_DATA_PATH = PROJECT_ROOT / "data_pipeline" / "output" / "clean_sales.csv"
