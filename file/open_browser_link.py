import pandas as pd
import subprocess
import os
import time

# === CONFIG ===
EXCEL_FILE = "file_url.xlsx"       # Excel file name
SHEET_NAME = 0                  # Sheet index or name
COLUMN_NAME = "URL"             # Column containing URLs
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"  # Update this path

# === Read Excel File ===
def read_urls(file, sheet, column):
    try:
        df = pd.read_excel(file, sheet_name=sheet)
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found.")
        return df[column].dropna().tolist()
    except Exception as e:
        print(f"Error reading Excel: {e}")
        return []

# === Open URL in Brave Private Window ===
def open_in_brave_private(url):
    try:
        subprocess.Popen([BRAVE_PATH, "--incognito", url])
    except Exception as e:
        print(f"Failed to open URL {url}: {e}")

# === Main ===
if __name__ == "__main__":
    urls = read_urls(EXCEL_FILE, SHEET_NAME, COLUMN_NAME)
    for url in urls:
        print(f"Opening: {url}")
        open_in_brave_private(url)
        time.sleep(1)  # Delay to avoid overwhelming the browser
