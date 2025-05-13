import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# Directory where the JSON file is stored
DATA_DIR = "django_automation/library"
os.makedirs(DATA_DIR, exist_ok=True)
DATA_FILE = os.path.join(DATA_DIR, "library_dict.json")

# Load and Save JSON
def load_library_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    data = []
                return data
            except json.JSONDecodeError:
                return []
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
        tk.Label(root, text="Search Import or Description:").pack(pady=5)
        self.search_entry = tk.Entry(root, width=40)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.perform_search)

        self.results_list = tk.Listbox(root, width=80, height=15)
        self.results_list.pack(pady=10)

        # --- Buttons ---
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Add Import", command=self.add_import_line).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Delete Selected", command=self.delete_selected_entry).grid(row=0, column=1, padx=5)

        self.perform_search()

    def perform_search(self, event=None):
        query = self.search_entry.get().lower()
        self.results_list.delete(0, tk.END)

        for entry in self.library_data:
            import_line = entry.get("import", "")
            description = entry.get("description", "")
            if query in import_line.lower() or query in description.lower():
                display = f"{import_line}  |  {description}"
                self.results_list.insert(tk.END, display)

    def add_import_line(self):
        # Prompt with a single input dialog for both import and description
        user_input = simpledialog.askstring(
            "Add Import",
            "Enter import and description separated by '&'\nExample: import os | Standard library for OS operations"
        )
        if not user_input:
            return

        # Split into import and description
        parts = user_input.split("&", 1)
        if len(parts) != 2:
            messagebox.showerror("Format Error", "Please use the format: import_statement & description")
            return

        import_line = parts[0].strip()
        description = parts[1].strip()

        # Check for duplicates
        for entry in self.library_data:
            if entry.get("import") == import_line:
                messagebox.showinfo("Exists", "This import line already exists.")
                return

        # Save new entry
        new_entry = {"import": import_line, "description": description}
        self.library_data.append(new_entry)
        save_library_data(self.library_data)
        self.perform_search()
    def delete_selected_entry(self):
        selection = self.results_list.curselection()
        print(f'delete result {selection}')
        if not selection:
            messagebox.showwarning("No Selection", "Select an import line to delete.")
            return

        idx = selection[0]
        selected_text = self.results_list.get(idx).split("  |  ")[0]

        for i, entry in enumerate(self.library_data):
            if entry.get("import") == selected_text:
                confirm = messagebox.askyesno("Confirm Delete", f"Delete import line?\n\n{selected_text}")
                if confirm:
                    del self.library_data[i]
                    save_library_data(self.library_data)
                    self.perform_search()
                return

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryReferenceApp(root)
    root.mainloop()
