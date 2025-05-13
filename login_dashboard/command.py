import pyperclip  
import pyautogui
import time 
from utilize import config

kibana, wingmarket = config['website']['kibana'], config['website']['wingmarket']
production, non_production = config['env']['production'], config['env']['non_production']

#Custom
def login_kibana():
    time.sleep(2)
    pyperclip.copy(config['database']['kibana_username'])
    pyautogui.hotkey('ctrl','v')
    pyautogui.hotkey('tab')
    pyperclip.copy(config['database']['kibana_password'])
    pyautogui.hotkey('ctrl','v')
    pyautogui.hotkey('enter')

#Custom
def login_wingmarket():
    time.sleep(1)
    pyautogui.hotkey('tab')
    pyperclip.copy(config['database']['wingmarket_username'])
    pyautogui.hotkey('ctrl','v')
    pyautogui.hotkey('tab')
    pyperclip.copy(config['database']['wingmarket_password'])
    pyautogui.hotkey('ctrl','v')
    pyautogui.hotkey('enter')

def redirect_url(func, url):
    func()
    pyperclip.copy(url)

    pyautogui.hotkey('ctrl', 'v')
    pyautogui.hotkey('ctrl', 'enter')
    
#Custom    
def get_website(action):
    actions = {
        kibana: login_kibana,
        wingmarket: login_wingmarket
    }
    return actions.get(action, lambda: "Unknown command")()

