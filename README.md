# Data Tools Suite

A modular Windows desktop GUI for Excel, CSV, TXT and JSON data utilities.

## Tools
- Compare Indexes
- Combine Excel + CSV
- Flatten JSON
- TXT → Excel
- Merge Data
- Infra Plots Report

## Run
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## Architecture
```
app/
├── main.py
├── modules/
│   ├── compare_indexes.py
│   ├── combine_files.py
│   ├── json_flatten.py
│   ├── txt_to_xlsx.py
│   ├── data_merge.py
│   └── infra_plots.py
└── utils/
    ├── gui.py
    └── io.py
```

The GUI is the only entry point. Processing logic lives in independent modules and shared file/dialog helpers are centralized in `utils`.
