from pathlib import Path
import pandas as pd

TXT_COLUMNS = [
    "col0","meter_id","timestamp","value","lat","lon","col6","meter_type","meter_data",
    "col9","col10","col11","col12","col13","col14","col15","col16","flag1","flag2","flag3","extra"
]

def load_merge_file(path):
    path = Path(path)
    ext = path.suffix.lower()
    if ext == ".csv":
        return pd.read_csv(path, dtype=str)
    if ext in {".xlsx", ".xls"}:
        return pd.read_excel(path, dtype=str)
    if ext == ".txt":
        return pd.read_csv(path, sep=";", header=None, names=TXT_COLUMNS,
                           skip_blank_lines=True, dtype=str)
    raise ValueError(f"Unsupported file type: {ext}")

def merge_all_columns(target_file, source_file):
    target, source = load_merge_file(target_file), load_merge_file(source_file)
    if target.shape[1] == 0 or source.shape[1] == 0:
        raise ValueError("Ένα από τα αρχεία δεν περιέχει στήλες.")
    kt, ks = target.columns[0], source.columns[0]
    merged = target.merge(source, left_on=kt, right_on=ks, how="left", suffixes=("", "_source"))
    if kt != ks and ks in merged.columns:
        merged.drop(columns=[ks], inplace=True)
    output = Path(target_file).with_name("merged_all_columns.xlsx")
    merged.to_excel(output, index=False)
    return output
