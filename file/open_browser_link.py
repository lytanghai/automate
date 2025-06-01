import pandas as pd
import subprocess
import os

# === CONFIG ===
EXCEL_FILE = "file_url.xlsx"      # Your Excel file
SHEET_NAME = 0                    # Sheet index or name
URL_COLUMN = "URL"
TITLE_COLUMN = "Title"
DESC_COLUMN = "Description"
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"  # Update path

# === Read and Validate Excel ===
def read_excel(file, sheet, url_col, title_col, desc_col):
    try:
        df = pd.read_excel(file, sheet_name=sheet)
        print("Available columns:", df.columns.tolist())
        required_cols = [url_col, title_col, desc_col]
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Column '{col}' not found in Excel.")
        df = df[required_cols].dropna()
        return df
    except Exception as e:
        print(f"Error reading Excel: {e}")
        return pd.DataFrame()

# === Display URLs, Titles, and Descriptions ===
def show_links(df):
    print("\nAvailable Links:\n")
    for idx, row in df.iterrows():
        print(f"{idx + 1}. [{row[TITLE_COLUMN]}] - {row[DESC_COLUMN]}\n    ↪ {row[URL_COLUMN]}\n")

# === Open URL in Brave Incognito ===
def open_brave(url):
    try:
        subprocess.Popen([BRAVE_PATH, "--incognito", url])
    except Exception as e:
        print(f"Error opening URL {url}: {e}")

# === Main Flow ===
if __name__ == "__main__":
    is_quit = False
    while True:

        df = read_excel(EXCEL_FILE, SHEET_NAME, URL_COLUMN, TITLE_COLUMN, DESC_COLUMN)
        if df.empty:
            exit()

        show_links(df)

        # Ask user which links to open
        selection = input("\nEnter number(s) to open (e.g., 1,3 or 'all'): ").strip().lower()
        if selection == 'q' or selection == 'quit':
            break
            
        if selection == 'all':
            for url in df[URL_COLUMN]:
                open_brave(url)
        else:
            try:
                indices = [int(i.strip()) - 1 for i in selection.split(",")]
                for i in indices:
                    if 0 <= i < len(df):
                        open_brave(df.iloc[i][URL_COLUMN])
                    else:
                        print(f"Index {i + 1} is out of range.")
            except ValueError:
                print("Invalid input. Please enter numbers like 1,2,3,'all', or q to quit.")
