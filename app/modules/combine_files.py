from pathlib import Path
import re
import pandas as pd

ID_8 = re.compile(r"\b0\d{7}\b")
ID_16 = re.compile(r"\b[A-Za-z0-9]{16}\b")

def extract_identifier(row):
    text = " ".join(map(str, row))
    match = ID_8.search(text) or ID_16.search(text)
    return match.group(0) if match else ""

def combine_excel_csv(folder):
    folder = Path(folder)
    frames, errors = [], []
    files = [p for p in folder.rglob("*")
             if p.suffix.lower() in {".xlsx", ".csv"} and p.name != "combined_data.xlsx"]
    for path in files:
        try:
            df = (pd.read_excel(path, dtype=str) if path.suffix.lower() == ".xlsx"
                  else pd.read_csv(path, dtype=str, encoding="utf-8", sep=None, engine="python"))
            df = df.fillna("")
            rel = path.parent.relative_to(folder)
            source = str(rel) if str(rel) != "." else "Κύριος_Φάκελος"
            extra = pd.DataFrame({
                "Πηγή_Φακέλου": [source] * len(df),
                "Πηγή_Αρχείου": [path.name] * len(df),
                "Αναγνωριστικό": [extract_identifier(row) for _, row in df.iterrows()]
            }, index=df.index)
            frames.append(pd.concat([extra, df], axis=1))
        except Exception as exc:
            errors.append(f"{path.name}: {exc}")
    if not frames:
        raise ValueError("Δεν βρέθηκαν έγκυρα .xlsx ή .csv αρχεία.")
    output = folder / "combined_data.xlsx"
    pd.concat(frames, ignore_index=True).to_excel(output, index=False)
    return output, errors
