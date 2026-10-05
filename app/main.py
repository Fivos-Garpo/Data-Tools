import tkinter as tk
from tkinter import ttk
from app.modules.compare_indexes import compare_first_column
from app.modules.combine_files import combine_excel_csv
from app.modules.json_flatten import flatten_json_columns
from app.modules.txt_to_xlsx import txt_to_xlsx
from app.modules.data_merge import merge_all_columns
from app.modules.infra_plots import generate_infra_report
from app.utils.gui import select_file, select_files, select_folder, show_error, show_info, ask_yes_no

TOOLS = [
    ("Compare Indexes","Compare the first Excel column against multiple Excel files.","compare"),
    ("Combine Excel + CSV","Combine a folder of Excel/CSV files and extract identifiers.","combine"),
    ("Flatten JSON","Detect and flatten JSON columns.","json"),
    ("TXT → Excel","Extract the JSON array from an Infra TXT export.","txt"),
    ("Merge Data","Merge target/source files using their first column.","merge"),
    ("Infra Plots Report","Create SNR, RSSI, SF and Noise Floor Excel reports.","plots"),
]
EXCEL=[("Excel files","*.xlsx *.xls")]
ANY=[("Supported files","*.xlsx *.xls *.csv *.txt *.json"),("All files","*.*")]
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Tools Suite")
        self.geometry("920x650")
        self.minsize(820,580)
        self.configure(bg="#10151c")
        self._style()
        self._build()
    def _style(self):
        s=ttk.Style(self); s.theme_use("clam")
        s.configure("TFrame",background="#10151c")
        s.configure("Card.TFrame",background="#18212b")
        s.configure("Title.TLabel",background="#10151c",foreground="#f4f7fb",font=("Segoe UI",26,"bold"))
        s.configure("Sub.TLabel",background="#10151c",foreground="#9ca9b8",font=("Segoe UI",11))
        s.configure("CardTitle.TLabel",background="#18212b",foreground="#fff",font=("Segoe UI",13,"bold"))
        s.configure("CardText.TLabel",background="#18212b",foreground="#aeb9c7",font=("Segoe UI",10))
        s.configure("Accent.TButton",font=("Segoe UI",10,"bold"),padding=(14,8))
    def _build(self):
        h=ttk.Frame(self); h.pack(fill="x",padx=36,pady=(30,18))
        ttk.Label(h,text="Data Tools Suite",style="Title.TLabel").pack(anchor="w")
        ttk.Label(h,text="Excel • CSV • TXT • JSON utilities",style="Sub.TLabel").pack(anchor="w",pady=(4,0))
        box=ttk.Frame(self); box.pack(fill="both",expand=True,padx=36,pady=10)
        for i in range(2): box.columnconfigure(i,weight=1)
        for i in range(3): box.rowconfigure(i,weight=1)
        for i,(title,desc,action) in enumerate(TOOLS):
            card=ttk.Frame(box,style="Card.TFrame",padding=20); card.grid(row=i//2,column=i%2,sticky="nsew",padx=8,pady=8)
            ttk.Label(card,text=title,style="CardTitle.TLabel").pack(anchor="w")
            ttk.Label(card,text=desc,style="CardText.TLabel",wraplength=350).pack(anchor="w",pady=(10,18))
            ttk.Button(card,text="Open Tool",style="Accent.TButton",command=lambda a=action:self.run(a)).pack(anchor="w")
        ttk.Label(self,text="Modular • Reusable • VS Code friendly",style="Sub.TLabel").pack(pady=(4,22))
    def run(self, action):
        try:
            if action=="compare":
                main=select_file("Select main Excel file",EXCEL)
                if not main:return
                files=select_files("Select comparison Excel files",EXCEL)
                if files: show_info(f"Completed!\n\n{compare_first_column(main,files)}")
            elif action=="combine":
                folder=select_folder("Select folder containing Excel/CSV files")
                if folder:
                    out,errors=combine_excel_csv(folder)
                    show_info(f"Completed!\n\n{out}\n\nSkipped: {len(errors)}")
            elif action=="json":
                file=select_file("Select CSV or Excel file",[( "CSV/Excel","*.csv *.xlsx *.xls")])
                if file:
                    out,cols=flatten_json_columns(file); show_info(f"Completed!\n\nJSON columns: {len(cols)}\n{out}")
            elif action=="txt":
                file=select_file("Select Infra TXT file",[( "Text files","*.txt")])
                if file: show_info(f"Completed!\n\n{txt_to_xlsx(file)}")
            elif action=="merge":
                target=select_file("Select TARGET file",ANY)
                if not target:return
                source=select_file("Select SOURCE file",ANY)
                if source: show_info(f"Completed!\n\n{merge_all_columns(target,source)}")
            elif action=="plots":
                files=select_files("Select Infra JSON/TXT/CSV files",[( "Infra files","*.json *.txt *.csv")])
                if files:
                    per_device=ask_yes_no("Per-device sheets","Create per-device sheets?")
                    show_info(f"Completed!\n\n{generate_infra_report(files,per_device=per_device)}")
        except Exception as exc:
            show_error(str(exc))
