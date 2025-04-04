import pytesseract
from PIL import ImageGrab
import pyautogui
import pygetwindow as gw
import time
import psutil
import os
import pyperclip

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


def copy_invoice_id(start_index, cell_name):
    pyautogui.hotkey("ctrl", "g")
    time.sleep(1)

    cell_address = f"{cell_name}{start_index}"
    pyautogui.write(cell_address, interval=0.1)
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
    pyautogui.write(invoice_id, interval=0.1)
    time.sleep(1) 
    pyautogui.press("enter")

def click(x,y):
    pyautogui.click(x, y)

# def save_file(file_name):
#     pyautogui.hotkey("ctrl", "s")

# def close_file():
#     pyautogui.hotkey("alt", "f4")
# -----------------------------------------------------------------------------------------------
# Execute script

insert_remark_on_cell = "X"
insert_hash_id_on_cell = "Y"
invoice_id_on_cell = "N"
start_index = 3
header_index = start_index - 1
tab_name = "LogTrail - Kibana"
init_value = True
file_name_exc = "02-Apr-25-(USD)-Transaction Success but supplier not receive credit"
file_name = rf"D:\task\{file_name_exc}.xlsx"

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
    time.sleep(1)
    invoice_id = copy_invoice_id(start_index, invoice_id_on_cell)
    open_kibana_chrome_tab(tab_name)
    time.sleep(1)

    search_invoice(-1770, 1464, '"' + str(invoice_id).strip() + '"')
    time.sleep(1)

    delete_all()
    copied_result = copy_from_screen()
    time.sleep(1)
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
close_file()
fill_no_call_in_column_s_string(file_name, insert_remark_on_cell)