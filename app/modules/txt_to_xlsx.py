from pathlib import Path
import json
import re
import pandas as pd

def txt_to_xlsx(txt_file):
    path = Path(txt_file)
    content = path.read_text(encoding="utf-8")
    match = re.search(r"\[.*\]", content, re.DOTALL)
    if not match:
        raise ValueError("Δεν βρέθηκε JSON array μέσα σε αγκύλες [].")
    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Μη έγκυρο JSON: {exc}") from exc
    output = path.with_suffix(".xlsx")
    pd.DataFrame(data).to_excel(output, index=False)
    return output
