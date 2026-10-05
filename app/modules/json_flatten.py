from pathlib import Path
import json
import pandas as pd

def flatten_json_columns(input_file):
    path = Path(input_file)
    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    elif path.suffix.lower() in {".xlsx", ".xls"}:
        df = pd.read_excel(path)
    else:
        raise ValueError("Input must be CSV or Excel.")
    columns = []
    for col in df.columns:
        sample = df[col].dropna().head(10)
        if any(str(v).strip().startswith(("{", "[")) for v in sample):
            columns.append(col)
    for col in columns:
        rows = []
        for value in df[col]:
            try:
                parsed = json.loads(str(value))
                if isinstance(parsed, list):
                    parsed = parsed[0] if parsed else {}
                rows.append(pd.json_normalize(parsed).to_dict("records")[0])
            except (json.JSONDecodeError, IndexError, TypeError):
                rows.append({})
        flat = pd.DataFrame(rows)
        flat.columns = [f"{col}_{name}" for name in flat.columns]
        df = pd.concat([df, flat], axis=1)
    output = path.with_name(f"{path.stem}_flattened.csv")
    df.to_csv(output, index=False)
    return output, columns
