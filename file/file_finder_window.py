import os
from pathlib import Path

def search_files(root_dir, name=None, ext=None):
    results = []

    if root_dir == "C":
        root_dir = "C:\\"
    elif root_dir == "D":
        root_dir = "D:\\"
    else:
        root_dir = str(Path.home() / "Desktop")
        
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Search directories
        if name and not ext:
            for d in dirnames:
                if d.lower() == name.lower():
                    results.append(os.path.join(dirpath, d))
        # Search files
        for f in filenames:
            fname, fext = os.path.splitext(f)
            if name and ext:
                if fname.lower() == name.lower() and fext.lower() == f".{ext.lower()}":
                    results.append(os.path.join(dirpath, f))
            elif name:
                if fname.lower() == name.lower():
                    results.append(os.path.join(dirpath, f))
            elif ext:
                if fext.lower() == f".{ext.lower()}":
                    results.append(os.path.join(dirpath, f))
    return results

if __name__ == "__main__":
    root_dir = input("Enter root directory to search C | D (skip to find in Desktop) : ").strip()
    name = input("Enter name (without extension) to search for (or press Enter to skip): ").strip() or None
    ext = input("Enter extension (without dot, e.g., txt, py) to search for (or press Enter to skip): ").strip() or None

    matches = search_files(root_dir, name, ext)
    print(f"\nResult: {len(matches)} record(s) found!")

    if matches:
        target = f"{name or '*'}{'.' + ext if ext else ''}"
        print(f"{'FileName' if ext else 'Directory name'}: {target}")
        print("Path:")
        for idx, path in enumerate(matches, 1):
            print(f" {idx}. {path}")
