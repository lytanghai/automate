import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def organize_by_extension(source_folder, log_output):
    if not os.path.isdir(source_folder):
        messagebox.showerror("Error", "Invalid folder path")
        return

    moved_files = 0
    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)

        # Skip directories and hidden/system files
        if os.path.isdir(file_path) or filename.startswith('.'):
            continue

        # Get file extension
        _, ext = os.path.splitext(filename)
        ext = ext[1:].lower() or "no_extension"

        # Create target folder
        target_dir = os.path.join(source_folder, ext)
        os.makedirs(target_dir, exist_ok=True)

        # Move file
        new_path = os.path.join(target_dir, filename)
        shutil.move(file_path, new_path)
        log_output.insert(tk.END, f"Moved: {filename} → {ext}/\n")
        moved_files += 1

    log_output.insert(tk.END, f"\n✅ Done. Total files moved: {moved_files}\n")
    log_output.see(tk.END)

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_path)

def start_organizing():
    folder = folder_entry.get().strip()
    log_output.delete('1.0', tk.END)
    organize_by_extension(folder, log_output)

# GUI setup
root = tk.Tk()
root.title("File Organizer by Extension")
root.geometry("600x500")

frame = tk.Frame(root)
frame.pack(pady=10)

folder_entry = tk.Entry(frame, width=50)
folder_entry.pack(side=tk.LEFT, padx=(10, 5))

browse_button = tk.Button(frame, text="Browse", command=browse_folder)
browse_button.pack(side=tk.LEFT)

organize_button = tk.Button(root, text="Organize Files", command=start_organizing)
organize_button.pack(pady=5)

log_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=25, font=("Consolas", 10))
log_output.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()
