import pyautogui
import pyperclip
import time

import re
import json

from util.transform import convert_log_to_json

def search_by_keyword(keyword):
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'f')
    pyautogui.write(keyword)


def extract_json_from_log(text):
    text = re.sub(r"WM\s*LogTrail\s*w", "", text)
    text = re.sub(r"access\s+denied.*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"Oldest event reached.*", "", text, flags=re.IGNORECASE)

    return text[:-1] if text else text


def split_log_by_timestamp(text):
    pattern = r"(?=\b[A-Z][a-z]{2} \d{2} \d{2}:\d{2}:\d{2} :)"
    chunks = re.split(pattern, text)
    return [chunk.strip() for chunk in chunks if chunk.strip()]

def copy_from_screen():
    pyautogui.moveTo(-1200, 780)
    pyautogui.click(-1200, 780)
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    copied_text = pyperclip.paste()
    return split_log_by_timestamp(extract_json_from_log(copied_text[:10000]))


def verify_chunk(chunk):
    if '/api/invoice/callback' in chunk:
        json_data = convert_log_to_json(chunk) 
        if json_data:
            if json_data.get("hash_id") == 'N/A':
                return 'hash id is empty'
            else:
                return json_data.get("hash_id")
    return None

def verify_success_callback_chunk(chunk):
    if 'http-outgoing response 200' in chunk and '/api/transactions/execute' in chunk:
        return True
    return False    