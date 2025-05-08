import os
import tkinter as tk
from tkinter import filedialog, scrolledtext

class FileTreeViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("File Tree Viewer")
        self.set_window_geometry()  # Call method to dynamically set window size and position
        self.hidden_dirs = set()
        self.checkbox_vars = {}

        # Search Entry and Button
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(root, textvariable=self.search_var, width=50)
        self.search_entry.pack(pady=10)

        self.search_button = tk.Button(root, text="Search", command=self.search_files)
        self.search_button.pack(pady=5)

        self.browse_button = tk.Button(root, text="Browse Folder", command=self.browse_folder)
        self.browse_button.pack(pady=10)

        self.checkbox_frame = tk.Frame(root)
        self.checkbox_frame.pack(pady=5)

        self.output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=30, font=("Consolas", 10))
        self.output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def set_window_geometry(self):
        # Get the width and height of the screen from the root (tk.Tk instance)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set the window size to 80% of the screen size (you can adjust as needed)
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)

        # Center the window on the screen
        position_top = int(screen_height / 2 - window_height / 2)
        position_left = int(screen_width / 2 - window_width / 2)

        # Set the window geometry
        self.root.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")
        
    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, folder_path + '\n')

            # Reset checkboxes
            for widget in self.checkbox_frame.winfo_children():
                widget.destroy()
            self.checkbox_vars.clear()
            self.hidden_dirs = self.get_hidden_dirs(folder_path)

            # Add checkboxes for hidden directories
            for i, hidden in enumerate(sorted(self.hidden_dirs)):
                var = tk.BooleanVar(value=False)
                chk = tk.Checkbutton(self.checkbox_frame, text=hidden, variable=var, command=self.update_tree_display)
                row = i // 5  # Place checkboxes in rows (5 per row)
                column = i % 5  # Max 5 checkboxes per row
                chk.grid(row=row, column=column, padx=5, sticky="w")
                self.checkbox_vars[hidden] = var

            self.folder_path = folder_path
            self.update_tree_display()

    def get_hidden_dirs(self, start_path):
        hidden = set()
        for root, dirs, _ in os.walk(start_path):
            for d in dirs:
                if d.startswith('.'):
                    hidden.add(d)
        return hidden

    def update_tree_display(self):
        if not hasattr(self, "folder_path"):
            return
        tree_lines = self.print_tree(self.folder_path)
        self.output_text.delete('1.0', tk.END)  # Clear everything
        self.output_text.insert(tk.END, self.folder_path + '\n')  # Reinsert folder path
        self.output_text.insert(tk.END, "\n".join(tree_lines))

    def should_include(self, dir_name):
        # Return whether the directory should be included based on checkbox status
        return self.checkbox_vars.get(dir_name, tk.BooleanVar(value=False)).get()

    def print_tree(self, start_path, prefix=""):
        lines = []
        try:
            items = os.listdir(start_path)
        except PermissionError:
            return lines  # skip directories without permission

        items.sort()
        items = [i for i in items if not i.startswith('.') or self.should_include(i)]

        for index, item in enumerate(items):
            path = os.path.join(start_path, item)
            connector = "└── " if index == len(items) - 1 else "├── "
            lines.append(prefix + connector + item)
            if os.path.isdir(path):
                extension = "    " if index == len(items) - 1 else "│   "
                lines.extend(self.print_tree(path, prefix + extension))
        return lines

    def search_files(self):
        search_term = self.search_var.get()
        if not search_term:
            return

        # Remove previous highlights
        self.output_text.tag_remove("highlight", "1.0", tk.END)

        # Get all the text from the output
        all_text = self.output_text.get("1.0", tk.END)
        start_index = "1.0"

        # Loop through the text and find all occurrences of the search term
        while True:
            start_index = self.output_text.search(search_term, start_index, stopindex=tk.END)
            if not start_index:
                break

            end_index = f"{start_index}+{len(search_term)}c"
            self.output_text.tag_add("highlight", start_index, end_index)
            self.output_text.tag_config("highlight", background="yellow", foreground="black")

            # Scroll to the found term
            self.output_text.yview_pickplace(start_index)
            start_index = end_index

if __name__ == "__main__":
    root = tk.Tk()
    app = FileTreeViewer(root)
    root.mainloop()
