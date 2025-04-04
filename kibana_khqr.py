import pytesseract
from PIL import ImageGrab
import pyautogui
import pygetwindow as gw
import time
import psutil
import os
import sys
import pyperclip

from datetime import datetime

from util.hotkey import press_tab
from util.hotkey import delete_all
from util.hotkey import save_file
from util.hotkey import close_file

from util.search import search_by_keyword
from util.search import copy_from_screen
from util.search import verify_chunk
from util.search import verify_success_callback_chunk

from util.file import open_excel
from util.file import insert_value
from util.file import count_excel_rows
from util.file import focus_excel_full_screen
from util.file import fill_no_call_in_column_s_string
from util.file import open_excel_find_invoice_id
from util.file import find_first_empty_cell_in_row

def copy_invoice_id(start_index, cell_name):
    pyautogui.hotkey("ctrl", "g")
    time.sleep(1)

    cell_address = f"{cell_name}{start_index}"
    pyperclip.copy(cell_address)
    pyautogui.hotkey("ctrl", "v")
    # pyautogui.write(cell_address, interval=0.1)
    time.sleep(1)

    pyautogui.press("enter")
    time.sleep(1)

    pyautogui.hotkey("ctrl", "c")
    time.sleep(1) 

    invoice_id = pyperclip.paste()

    return invoice_id

def open_kibana_chrome_tab(tab_name):
    for process in psutil.process_iter(['name']):
        if process.info['name'] and 'chrome' in process.info['name'].lower():
            break
    else:
        print("Chrome is not running.")
        return False

    # Get all Chrome windows
    chrome_windows = gw.getWindowsWithTitle(tab_name)

    for window in chrome_windows:
        if tab_name in window.title:
            print(f"Tab '{tab_name}' found in Chrome.")
            window.activate()
            time.sleep(1)
            return True

    print(f"No Chrome tab with title '{tab_name}' found.")
    return False

def search_invoice(x,y, invoice_id):
    pyautogui.click(x, y)
    delete_all()
    time.sleep(1) 
    pyperclip.copy(invoice_id)
    pyautogui.hotkey("ctrl", "v")

    time.sleep(1) 
    pyautogui.press("enter")

def click(x,y):
    pyautogui.click(x, y)

# -----------------------------------------------------------------------------------------------
# Execute script

file_name_exc = ""
if len(sys.argv) > 1:
    file_name_exc = sys.argv[1]
    print(f"The parameter is: {file_name_exc}")
else:
    print("must input file name!")
    exit()

file_name = rf"D:\task\{file_name_exc}.xlsx"

current_time = datetime.now().strftime("%d/%m/%Y : %I:%M:%S %p")

print(f"""
FILE NAME: {file_name_exc}.xlsx
STARTED BY: {os.getlogin()}
DATE: {current_time}
""")

tab_name = "LogTrail - Kibana"
init_value = True
start_index = 3
insert_remark_on_cell, insert_hash_id_on_cell = find_first_empty_cell_in_row(file_name, 2)
invoice_id_on_cell = open_excel_find_invoice_id(file_name, "invoice_id")

header_index = start_index - 1

focus_excel_full_screen(file_name)

total_rows = count_excel_rows(file_name, start_index)
print(f"Total Rows to Process: {total_rows}")

time.sleep(1)

if init_value:
    click(-1238, 170)
    insert_value(file_name, insert_remark_on_cell, header_index, 'Result')
    insert_value(file_name, insert_hash_id_on_cell, header_index, "Txn first paid")
    init_value = False

for i in range(total_rows):
    time.sleep(0.5)
    invoice_id = copy_invoice_id(start_index, invoice_id_on_cell)
    time.sleep(0.5)
    open_kibana_chrome_tab(tab_name)
    time.sleep(0.5)
    search_invoice(-1770, 1464, '"' + str(invoice_id).strip() + '"')
    time.sleep(1.5)

    delete_all()
    copied_result = copy_from_screen()
    
    focus_excel_full_screen(file_name)
    hash_id = ''

    for index, chunk in enumerate(copied_result):
        hash_id = verify_chunk(chunk)
        is_executed_payment = verify_success_callback_chunk(chunk)

        if hash_id or is_executed_payment:
            if hash_id is None and is_executed_payment:
                hash_id = 'No Response hash_id from core'
            click(-1238, 170)
            insert_value(file_name, insert_remark_on_cell, start_index, 'Invoice already paid')
            insert_value(file_name, insert_hash_id_on_cell, start_index, hash_id)
            break

    start_index += 1 

save_file(file_name)
print("File is saved successfully!")
time.sleep(2)
close_file()
fill_no_call_in_column_s_string(file_name, insert_remark_on_cell)