import pyperclip  
import pyautogui
import time 
from utilize import config, production, non_production
from utilize import kibana, wingmarket, wing_digital, wing_helpdesk

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

#Custom
def login_wing_digital():
    time.sleep(1)
    for i in range(0,2):
        pyautogui.hotkey('tab')

    time.sleep(1)
    pyperclip.copy(config['database']['wing_digital_username'])
    pyautogui.hotkey('ctrl','v')
    pyautogui.hotkey('tab')
    pyperclip.copy(config['database']['wing_digital_password'])
    pyautogui.hotkey('ctrl','v')
    pyautogui.hotkey('enter')

#Custom
def login_wing_helpdesk():
    time.sleep(1)
    pyperclip.copy(config['database']['wing_helpdesk_username'])
    pyautogui.hotkey('ctrl','v')
    
    pyautogui.hotkey('tab')
    pyperclip.copy(config['database']['wing_helpdesk_password'])
    pyautogui.write(pyperclip.paste(), interval=0.05)
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
        wingmarket: login_wingmarket,
        wing_digital: login_wing_digital,
        wing_helpdesk: login_wing_helpdesk
    }
    return actions.get(action, lambda: "Unknown command")()

