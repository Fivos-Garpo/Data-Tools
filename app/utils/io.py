from pathlib import Path
import pandas as pd

def read_table(path, txt_columns=None):
    path = Path(path)
    ext = path.suffix.lower()
    if ext == ".csv":
        return pd.read_csv(path, dtype=str, sep=None, engine="python")
    if ext in {".xlsx", ".xls"}:
        return pd.read_excel(path, dtype=str)
    if ext == ".txt" and txt_columns:
        return pd.read_csv(path, sep=";", header=None, names=txt_columns,
                           skip_blank_lines=True, dtype=str)
    raise ValueError(f"Unsupported file type: {path.suffix}")
