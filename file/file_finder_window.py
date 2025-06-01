import os
import sys
import time
import threading
from pathlib import Path

# === Spinner class for loading animation ===
class Spinner:
    def __init__(self, message="Searching..."):
        self.spinner = ["|", "/", "-", "\\"]
        self.idx = 0
        self.running = False
        self.thread = None
        self.message = message
        self.current_dir = ""

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.animate)
        self.thread.start()

    def animate(self):
        while self.running:
            spin_char = self.spinner[self.idx % len(self.spinner)]
            sys.stdout.write(
                f"\r{self.message} {spin_char} {self.current_dir[:50]}..." + " " * 10
            )
            sys.stdout.flush()
            self.idx += 1
            time.sleep(0.1)

    def update_dir(self, dirpath):
        self.current_dir = dirpath

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        sys.stdout.write("\r✅ Done scanning.                              \n")

# === File search function with spinner ===
def search_files(root_dir, name=None, ext=None):
    results = []
    spinner = Spinner("Scanning")

    # Interpret predefined options
    if root_dir.strip().upper() == "C":
        root_dir = "C:\\"
    elif root_dir.strip().upper() == "D":
        root_dir = "D:\\"
    elif not root_dir:
        root_dir = str(Path.home() / "Desktop")

    if not os.path.exists(root_dir):
        print(f"❌ Path does not exist: {root_dir}")
        return []

    spinner.start()

    try:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            spinner.update_dir(dirpath)

            for f in filenames:
                fname, fext = os.path.splitext(f)
                fname_lower = fname.lower()
                fext_lower = fext.lower().lstrip(".")

                # Match logic:
                # - name in fname
                # - ext matches if provided
                if name and name.lower() in fname_lower:
                    if ext:
                        if ext.lower() == fext_lower:
                            results.append(os.path.join(dirpath, f))
                    else:
                        results.append(os.path.join(dirpath, f))
                elif not name and ext and ext.lower() == fext_lower:
                    results.append(os.path.join(dirpath, f))

            # Optional: search directory names by partial match
            if name and not ext:
                for d in dirnames:
                    if name.lower() in d.lower():
                        results.append(os.path.join(dirpath, d))

    finally:
        spinner.stop()

    return results


# === Main Entry Point ===
if __name__ == "__main__":
    print("📁 Search in C, D, Desktop, or enter full path (e.g. C:\\Users\\ASUS\\Documents):")
    root_dir = input("Enter root directory: ").strip()

    name = input("Enter name (without extension) to search for (or press Enter to skip): ").strip() or None
    ext = input("Enter extension (without dot, e.g., txt, py) to search for (or press Enter to skip): ").strip() or None

    matches = search_files(root_dir, name, ext)
    print(f"\n🔍 Result: {len(matches)} record(s) found!")

    if matches:
        target = f"{name or '*'}{'.' + ext if ext else ''}"
        print(f"{'FileName' if ext else 'Directory name'}: {target}")
        print("Path(s):")
        for idx, path in enumerate(matches, 1):
            print(f" {idx}. {path}")
