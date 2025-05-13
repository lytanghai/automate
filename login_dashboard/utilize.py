import pyperclip  
import pyautogui
import subprocess
import time 
import configparser
import os

config = configparser.ConfigParser()

if os.path.exists('settings.config'):
    config.read('settings.config')
else:
    print("Config file not found.")


def open_chrome_tab():
    subprocess.Popen([
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "--new-tab",
        "https://www.google.com"
    ])
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'l')


#Custom
def show_endpoint():
    print("-----------------------------------")
    print("NON PRODUCTION")
    print('1.1 Kibana')
    print("-----------------------------------")
    print("PRODUCTION")
    print('2.1. Kibana')
    print('2.2 Wing Market')
    print("-----------------------------------")





