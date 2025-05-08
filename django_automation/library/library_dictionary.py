import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# Directory where the JSON file is stored
DATA_DIR = "django_automation/library"
os.makedirs(DATA_DIR, exist_ok=True)  # Create if not exists
DATA_FILE = os.path.join(DATA_DIR, "library_dict.json")
test = ""

def unused():
    pass
# Load and Save JSON
def load_library_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            # Ensure we load it as a list, not a dict
            data = json.load(f)
            if not isinstance(data, list):
                data = []  # In case the file contains a dict instead of a list
            return data
    return []

def save_library_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

class LibraryReferenceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Import Reference")

        self.library_data = load_library_data()

        # --- Widgets ---
        tk.Label(root, text="Search Import:").pack(pady=5)
        self.search_entry = tk.Entry(root, width=40)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.perform_search)

        self.results_list = tk.Listbox(root, width=60, height=15)
        self.results_list.pack(pady=10)

        # --- Buttons ---
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Add Import", command=self.add_import_line).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Delete Selected", command=self.delete_selected_entry).grid(row=0, column=1, padx=5)

    def perform_search(self, event=None):
        query = self.search_entry.get().lower()
        self.results_list.delete(0, tk.END)

        for imp in self.library_data:
            if query in imp.lower():
                self.results_list.insert(tk.END, imp)

    def add_import_line(self):
        # Ask for the complete import line
        import_line = simpledialog.askstring("Import Line", "Enter the import line (e.g., 'import tkinter' or 'from tkinter import filedialog'):")
        if not import_line:
            return

        import_line = import_line.strip()

        # Check if the import line already exists
        if import_line not in self.library_data:
            self.library_data.append(import_line)
            save_library_data(self.library_data)
            # messagebox.showinfo("Success", "Import line added.")
            self.perform_search()
        else:
            messagebox.showinfo("Exists", "This import line already exists.")

    def delete_selected_entry(self):
        selection = self.results_list.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Select an import line to delete.")
            return

        idx = selection[0]
        import_line = self.library_data[idx]

        confirm = messagebox.askyesno("Confirm Delete", f"Delete import line?\n\n{import_line}")
        if confirm:
            del self.library_data[idx]
            save_library_data(self.library_data)
            self.perform_search()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryReferenceApp(root)
    root.mainloop()
