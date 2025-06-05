import tkinter as tk
from tkinter import ttk, messagebox
import re

class PseudoCodeParserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pseudo Code Tree Viewer")
        self.root.geometry("700x500")
        self.root.configure(bg="#1e1e1e")  # dark background

        self.input_text = tk.Text(root, height=15, bg="#2e2e2e", fg="white", insertbackground='white')
        self.input_text.pack(fill="x", padx=10, pady=5)

        self.parse_button = tk.Button(root, text="Parse Pseudo Code", command=self.parse_pseudo_code, bg="#333", fg="white")
        self.parse_button.pack(pady=5)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#1e1e1e",
                        foreground="white",
                        fieldbackground="#1e1e1e",
                        rowheight=25,
                        font=("Consolas", 10))
        style.map("Treeview", background=[("selected", "#444")])

        self.tree = ttk.Treeview(root)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.heading('#0', text='Pseudo Code Hierarchy', anchor='w')

        self.level_colors = {
            1: "white",
            2: "orange",
            3: "cyan",
            4: "lime",
            5: "orange",
            6: "magenta",
            7: "#00008B",     # dark blue
            8: "#8B0000",     # dark red
            9: "gray",
            10: "orange"
        }

    def parse_pseudo_code(self):
        self.tree.delete(*self.tree.get_children())
        lines = self.input_text.get("1.0", tk.END).strip().split('\n')

        level_node_map = {}
        root_id = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith('+ Feature:'):
                feature_name = line.split(':', 1)[1].strip()
                root_id = self.tree.insert('', 'end', text=feature_name, tags=('level0',))
                level_node_map.clear()
                level_node_map[""] = root_id
                self.tree.tag_configure('level0', foreground="white")
            else:
                match = re.match(r'^(\d+(\.\d+)*)(?:\s+)(.+)', line)
                if match:
                    level_str = match.group(1)
                    label = match.group(3)

                    level_depth = level_str.count('.') + 1
                    color = self.level_colors.get(level_depth, "white")

                    if '.' in level_str:
                        parent_level = '.'.join(level_str.split('.')[:-1])
                    else:
                        parent_level = ""

                    parent_id = level_node_map.get(parent_level)
                    if parent_id is None:
                        messagebox.showerror("Parsing Error", f"Missing parent for level {level_str}")
                        return

                    tag_name = f"level{level_depth}"
                    self.tree.tag_configure(tag_name, foreground=color)

                    node_id = self.tree.insert(parent_id, 'end', text=f"{level_str} {label}", tags=(tag_name,))
                    level_node_map[level_str] = node_id
                else:
                    messagebox.showwarning("Invalid Line", f"Line format not recognized: {line}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PseudoCodeParserApp(root)
    root.mainloop()
