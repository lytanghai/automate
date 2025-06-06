import tkinter as tk
from tkinter import scrolledtext, messagebox, Toplevel
import json

def compare_jsons():
    try:
        data1 = json.loads(input1.get("1.0", tk.END).strip())
        data2 = json.loads(input2.get("1.0", tk.END).strip())
    except json.JSONDecodeError as e:
        messagebox.showerror("Invalid JSON", f"Error parsing JSON:\n{e}")
        return

    formatted1 = json.dumps(data1, indent=4, sort_keys=True)
    formatted2 = json.dumps(data2, indent=4, sort_keys=True)

    output_win = Toplevel(root)
    output_win.title("Comparison Result")
    output_win.geometry("1200x700")
    output_win.rowconfigure(0, weight=1)
    output_win.columnconfigure([0, 1], weight=1, uniform='col')

    output_box1 = tk.Text(output_win, wrap=tk.NONE)
    output_box2 = tk.Text(output_win, wrap=tk.NONE)

    output_box1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    output_box2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    output_box1.insert(tk.END, formatted1)
    output_box2.insert(tk.END, formatted2)

    for box in (output_box1, output_box2):
        box.tag_config("diff", background="#FF6347", foreground="white")  # tomato red for differences
        box.tag_config("missing", background="#8B0000", foreground="white")  # dark red for missing keys
        box.config(state=tk.DISABLED)

    scrollbar = tk.Scrollbar(output_win, orient=tk.VERTICAL)
    scrollbar.grid(row=0, column=2, sticky='ns', pady=5)

    def on_scrollbar(*args):
        output_box1.yview(*args)
        output_box2.yview(*args)

    def on_scroll1(*args):
        output_box2.yview_moveto(args[0])
        scrollbar.set(*args)

    def on_scroll2(*args):
        output_box1.yview_moveto(args[0])
        scrollbar.set(*args)

    output_box1.config(yscrollcommand=on_scroll1)
    output_box2.config(yscrollcommand=on_scroll2)
    scrollbar.config(command=on_scrollbar)

    map1 = build_path_line_map(formatted1)
    map2 = build_path_line_map(formatted2)

    diff_paths = []

    # Recursively compare both JSON objects and collect paths with different values or missing keys
    def recursive_compare(o1, o2, path=()):
        if isinstance(o1, dict) and isinstance(o2, dict):
            keys1 = set(o1.keys())
            keys2 = set(o2.keys())
            for k in keys1.union(keys2):
                new_path = path + (k,)
                if k not in o1:
                    diff_paths.append(('missing_in_1', new_path))
                elif k not in o2:
                    diff_paths.append(('missing_in_2', new_path))
                else:
                    recursive_compare(o1[k], o2[k], new_path)
        elif isinstance(o1, list) and isinstance(o2, list):
            max_len = max(len(o1), len(o2))
            for i in range(max_len):
                new_path = path + (str(i),)
                if i >= len(o1):
                    diff_paths.append(('missing_in_1', new_path))
                elif i >= len(o2):
                    diff_paths.append(('missing_in_2', new_path))
                else:
                    recursive_compare(o1[i], o2[i], new_path)
        else:
            # Compare values with rules
            if not values_equal(o1, o2):
                diff_paths.append(('diff', path))

    def values_equal(v1, v2):
        # Numeric compare
        if is_number(v1) and is_number(v2):
            return float(v1) == float(v2)
        # Case-insensitive string compare
        if isinstance(v1, str) and isinstance(v2, str):
            return v1.lower() == v2.lower()
        # Otherwise strict compare
        return v1 == v2

    def is_number(v):
        return isinstance(v, (int, float))

    recursive_compare(data1, data2)

    def highlight_line(box, line_num, tag):
        box.config(state=tk.NORMAL)
        box.tag_add(tag, f"{line_num}.0", f"{line_num}.end")
        box.config(state=tk.DISABLED)

    def try_find_line(path_map, path):
        # Exact match
        if path in path_map:
            return path_map[path]
        # Remove trailing numeric indices (list indices) and try
        trimmed = tuple(x for x in path if not x.isdigit())
        if trimmed in path_map:
            return path_map[trimmed]
        # No match
        return None

    for diff_type, path in diff_paths:
        if diff_type == 'diff':
            line1 = try_find_line(map1, path)
            if line1:
                highlight_line(output_box1, line1, "diff")
            line2 = try_find_line(map2, path)
            if line2:
                highlight_line(output_box2, line2, "diff")
        elif diff_type == 'missing_in_1':
            line2 = try_find_line(map2, path)
            if line2:
                highlight_line(output_box2, line2, "missing")
        elif diff_type == 'missing_in_2':
            line1 = try_find_line(map1, path)
            if line1:
                highlight_line(output_box1, line1, "missing")


def build_path_line_map(formatted_json):
    path_map = {}
    stack = []
    indent_stack = []
    lines = formatted_json.splitlines()

    for i, line in enumerate(lines, 1):
        stripped = line.lstrip(' ')
        indent = (len(line) - len(stripped)) // 4

        while indent_stack and indent_stack[-1] >= indent:
            indent_stack.pop()
            stack.pop()

        if stripped.startswith('"'):
            key_end = stripped.find('":')
            if key_end != -1:
                key = stripped[1:key_end]
                stack.append(key)
                indent_stack.append(indent)
                path_map[tuple(stack)] = i
        elif stripped.startswith('- '):
            # Count sibling list items to get index
            count = 0
            for j in range(i-1, 0, -1):
                prev_line = lines[j-1].lstrip(' ')
                prev_indent = (len(lines[j-1]) - len(prev_line)) // 4
                if prev_indent < indent:
                    break
                if prev_line.startswith('- '):
                    count += 1
            stack.append(str(count))
            indent_stack.append(indent)
            path_map[tuple(stack)] = i

    return path_map


# --- GUI Setup ---
root = tk.Tk()
root.title("JSON Compare")
root.geometry("900x600")

tk.Label(root, text="JSON 1:").pack(anchor="w")
input1 = scrolledtext.ScrolledText(root, height=15)
input1.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

tk.Label(root, text="JSON 2:").pack(anchor="w")
input2 = scrolledtext.ScrolledText(root, height=15)
input2.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

compare_btn = tk.Button(root, text="Compare JSONs", command=compare_jsons, bg="blue", fg="white")
compare_btn.pack(fill=tk.X, padx=5, pady=10)

root.mainloop()
