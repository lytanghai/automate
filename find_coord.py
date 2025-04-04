import time
import pyautogui

while True:
    x, y = pyautogui.position()
    print(f"Mouse at: ({x}, {y})", end="\r", flush=True)
    time.sleep(0.1)