import os
from pathlib import Path
import sys
import time
import threading

# Spinner for loading animation
class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while True:
            for cursor in '|/-\\':
                yield cursor

    def __init__(self, message="Searching"):
        self.spinner_generator = self.spinning_cursor()
        self.message = message
        self.thread = threading.Thread(target=self.spin)

    def spin(self):
        while self.busy:
            sys.stdout.write(f"\r{self.message}... {next(self.spinner_generator)}")
            sys.stdout.flush()
            time.sleep(self.delay)

    def start(self):
        self.busy = True
        self.thread.start()

    def stop(self):
        self.busy = False
        self.thread.join()
        sys.stdout.write("\rDone!                  \n")
        sys.stdout.flush()

# Search function
def search_files(root_dir, name=None, ext=None):
    results = []
    spinner = Spinner("Scanning")

    # Normalize root directory
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
        for dirpath, _, filenames in os.walk(root_dir):
            for f in filenames:
                fname, fext = os.path.splitext(f)
                fname_lower = fname.lower()
                fext_lower = fext.lower().lstrip(".")

                if name and ext:
                    if name.lower() in fname_lower and ext.lower() == fext_lower:
                        results.append(os.path.join(dirpath, f))
                elif name and not ext:
                    if name.lower() in fname_lower:
                        results.append(os.path.join(dirpath, f))
                elif ext and not name:
                    if ext.lower() == fext_lower:
                        results.append(os.path.join(dirpath, f))
    finally:
        spinner.stop()

    return results

# === MAIN ===
if __name__ == "__main__":
    root_dir = input("🔍 Enter root directory (C | D | path | empty for Desktop): ").strip()
    name = input("🔠 Enter partial file name to search for (or press Enter to skip): ").strip() or None
    ext = input("📄 Enter extension (e.g., txt, pdf) to search for (or press Enter to skip): ").strip() or None

    matches = search_files(root_dir, name, ext)
    print(f"\n✅ Result: {len(matches)} record(s) found.")

    if matches:
        print("📁 Paths:")
        for idx, path in enumerate(matches, 1):
            print(f" {idx}. {path}")
    else:
        print("🚫 No matching files found.")
