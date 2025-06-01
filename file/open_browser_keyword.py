import pandas as pd
import subprocess
import os
import sys
import time

# === CONFIGURATION ===
EXCEL_FILE = "temp/keywords.xlsx"         # Path to Excel file
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
BATCH_SIZE = 5
DELAY_SECONDS = 45

# === Get CLI Param for Additional Search Term ===
extra_query = ""
if len(sys.argv) > 1:
    extra_query = " " + sys.argv[1]  # first argument = query addition

if len(sys.argv) > 2:
    try:
        DELAY_SECONDS = float(sys.argv[2])  # second argument = delay in seconds
    except ValueError:
        print("⚠ Invalid delay value. Using default delay of 45 seconds.")

# === FUNCTION TO LAUNCH DUCKDUCKGO SEARCH IN BRAVE INCOGNITO ===
def open_in_brave(query):
    try:
        full_query = f"{query}{extra_query}"
        search_url = f"https://duckduckgo.com/?q={full_query}"
        subprocess.Popen([BRAVE_PATH, "--incognito", search_url],
                         creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0)
        time.sleep(DELAY_SECONDS)
    except Exception as e:
        print(f"Error opening search for '{query}': {e}")

# === MAIN LOGIC ===
def main():
    try:
        df = pd.read_excel(EXCEL_FILE, usecols=[0], header=None)
        keywords = [str(cell).strip() for cell in df.iloc[:, 0] if pd.notna(cell) and str(cell).strip()]
    except Exception as e:
        print(f"Error reading Excel: {e}")
        return

    if not keywords:
        print("❌ No keywords found in the file.")
        return

    index = 0
    total = len(keywords)

    while 0 <= index < total:
        end = min(index + BATCH_SIZE, total)
        current_batch = keywords[index:end]

        print(f"\n🔎 Opening search for records {index+1} to {end} of {total}...\n")
        for term in current_batch:
            print(f"→ {term}{extra_query}")
            open_in_brave(term)

        if end == total:
            print("\n✅ End of list reached.")
            break

        user_input = input("\nType [n]ext, [p]revious, [q]uit: ").strip().lower()
        if user_input == 'n':
            index += BATCH_SIZE
        elif user_input == 'p':
            index = max(index - BATCH_SIZE, 0)
        elif user_input == 'q':
            print("👋 Exiting.")
            break
        else:
            print("Invalid input. Please type 'n', 'p', or 'q'.")

if __name__ == "__main__":
    main()
