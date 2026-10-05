from tkinter import filedialog, messagebox

def select_file(title, filetypes):
    return filedialog.askopenfilename(title=title, filetypes=filetypes)

def select_files(title, filetypes):
    return filedialog.askopenfilenames(title=title, filetypes=filetypes)

def select_folder(title):
    return filedialog.askdirectory(title=title)

def show_error(message):
    messagebox.showerror("Data Tools Suite", message)

def show_info(message):
    messagebox.showinfo("Data Tools Suite", message)

def ask_yes_no(title, message):
    return messagebox.askyesno(title, message)
