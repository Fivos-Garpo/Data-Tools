from pathlib import Path
import pandas as pd

def compare_first_column(main_file, comparison_files):
    main = pd.read_excel(main_file, dtype=str)
    if main.shape[1] == 0:
        raise ValueError("The main file has no columns.")
    main.iloc[:, 0] = main.iloc[:, 0].fillna("").astype(str).str.strip()
    found = {}
    main_values = set(main.iloc[:, 0])
    for file in comparison_files:
        df = pd.read_excel(file, dtype=str)
        if df.shape[1] == 0:
            continue
        values = set(df.iloc[:, 0].fillna("").astype(str).str.strip())
        for value in values & main_values:
            found.setdefault(value, []).append(Path(file).name)
    main["Found_in"] = main.iloc[:, 0].map(
        lambda value: " / ".join(found.get(value, [])) or None
    )
    output = Path(main_file).with_name(f"{Path(main_file).stem}_comparison.xlsx")
    main.to_excel(output, index=False)
    return output
