import tkinter as tk
from tkinter import scrolledtext


def extract_conditions(java_code: str) -> str:
    lines = java_code.splitlines()
    pseudo_code = []
    indent_level = 0

    def add_line(line):
        pseudo_code.append("    " * indent_level + line.strip())

    for raw_line in lines:
        line = raw_line.strip()

        if not line or line.startswith("//"):
            continue

        if line.startswith("}"):
            indent_level = max(indent_level - 1, 0)

        if line.startswith("if"):
            condition = line.split("if", 1)[1].split("{")[0].strip()
            add_line(f"IF {condition}")
        elif line.startswith("else if"):
            condition = line.split("else if", 1)[1].split("{")[0].strip()
            add_line(f"ELSE IF {condition}")
        elif line.startswith("else"):
            add_line("ELSE")
        elif line.startswith("switch"):
            condition = line.split("switch", 1)[1].split("{")[0].strip()
            add_line(f"SWITCH {condition}")
        elif line.startswith("case"):
            condition = line.split("case", 1)[1].strip(":").strip()
            add_line(f"CASE {condition}")
        elif line.startswith("default"):
            add_line("DEFAULT")

        if "{" in line:
            indent_level += 1
        if "}" in line and not line.startswith("}"):
            indent_level = max(indent_level - 1, 0)

    return "\n".join(pseudo_code)


def convert():
    java_code = input_text.get("1.0", tk.END)
    result = extract_conditions(java_code)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)


# GUI Setup
window = tk.Tk()
window.title("Java Filter Condition & Switch Case")
window.geometry("800x600")

# Input Area
tk.Label(window, text="Paste Java Function Below:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
input_text = scrolledtext.ScrolledText(window, height=15, font=("Courier", 10))
input_text.pack(fill="both", expand=True, padx=10, pady=5)

# Convert Button
convert_btn = tk.Button(window, text="Filter", command=convert, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
convert_btn.pack(pady=10)

# Output Area
tk.Label(window, text="Extracted Pseudo Code:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
output_text = scrolledtext.ScrolledText(window, height=15, font=("Courier", 10), bg="#f4f4f4")
output_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

# Start GUI
window.mainloop()
