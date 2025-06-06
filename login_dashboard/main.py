import subprocess
import pyautogui
import pyperclip  
import time 

import tkinter as tk
from utilize import show_endpoint, open_chrome_tab, config, production, non_production
from command import get_website, login_kibana, redirect_url
from utilize import kibana, wingmarket, wing_digital, wing_helpdesk


#*1
WEBSITE = {
    production: {
        kibana: "https://logging.wingmarket.com/app/logtrail#/?q=*&h=All&t=Now&i=invoicing*&_g=()",
        wingmarket: "https://portal.wingmarket.com/",
        wing_digital: "https://wingdigital.com/auth/login?returnUrl=/dashboard",
        wing_helpdesk: "https://webhelpdesk.wingbank.com.kh:8283/HomePage.do"
    },
    non_production: {

    }
}

def command_env(input):
    input = int(str(input.split('.')[0]))
    if input == 1:
        return non_production
    elif input == 2:
        return production
    else:
        return "default"
    
#*2
def command_web(input):
    input = int(str(input).split('.')[1])

    if input == 1:
        return kibana
    elif input == 2:
        return wingmarket
    elif input == 3:
        return wing_digital
    elif input == 4:
        return wing_helpdesk
    else:
        return "default"
        

if __name__ == "__main__":
    #Script
    
    # show_endpoint()

    #11111111
    # website = str(input("pick: "))

    # env = command_env(website)
    # val = command_web(website)

    # redirect_url(open_chrome_tab, WEBSITE[env][val])
    # get_website(val)
    
    #222222222 for testing
    # redirect_url(open_chrome_tab, WEBSITE[production][wingmarket])
    # get_website(wingmarket)
    # End of Script

    #GUI
    #*4
    website_map = {
        "Prod Kibana": "2.1",
        "Prod Wingmarket": "2.2",
        "Prod Wing Digital": "2.3",
        "Prod Wing Helpdesk": "2.4",
        "Dev C": "4.1",
        "Dev D": "4.2",
        "Dev E": "5.1",
        "Dev F": "5.2",
        "Dev G": "6.1",
        "Dev H": "6.2",
    }

    # When a button is clicked
    def on_button_click(label):
        website = website_map[label]
        env = command_env(website)
        val = command_web(website)
        redirect_url(open_chrome_tab, WEBSITE[env][val])
        get_website(val)

    # Create the UI
    root = tk.Tk()
    root.title("Auto Login")
    root.geometry("1000x1000")
    root.configure(bg="#1c1c1c")

    tk.Label(root, text="Auto Login", fg="white", bg="#1c1c1c", font=("Comic Sans MS", 16)).pack(pady=10)

    grid_frame = tk.Frame(root, bg="#1c1c1c")
    grid_frame.pack()

    max_rows = 10
    for i, label in enumerate(website_map.keys()):
        row = i % max_rows
        col = i // max_rows

        bg_color = "#f08b12" if "Prod" in label else "green"
        fg_color = "white"

        tk.Button(
            grid_frame,
            text=label,
            width=20,
            height=2,
            font=("Comic Sans MS", 12),
            bg=bg_color,
            fg=fg_color,
            command=lambda lbl=label: on_button_click(lbl)
        ).grid(row=row, column=col, padx=1, pady=5)

    root.mainloop()
