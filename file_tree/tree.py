import os
import tkinter as tk
from tkinter import filedialog, scrolledtext

def print_tree(start_path, prefix=""):
    lines = []
    items = os.listdir(start_path)
    items.sort()
    for index, item in enumerate(items):
        path = os.path.join(start_path, item)
        connector = "└── " if index == len(items) - 1 else "├── "
        lines.append(prefix + connector + item)
        if os.path.isdir(path):
            extension = "    " if index == len(items) - 1 else "│   "
            lines.extend(print_tree(path, prefix + extension))
    return lines

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_text.delete('1.0', tk.END)
        output_text.insert(tk.END, folder_path + '\n')
        tree_lines = print_tree(folder_path)
        output_text.insert(tk.END, "\n".join(tree_lines))

# GUI Setup
root = tk.Tk()
root.title("File Tree Viewer")
root.geometry("600x500")

browse_button = tk.Button(root, text="Browse Folder", command=browse_folder)
browse_button.pack(pady=10)

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=25, font=("Consolas", 10))
output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()
