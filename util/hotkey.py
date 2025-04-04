import pyautogui

def press_tab():
  """Presses the Tab key using pyautogui."""
  try:
    pyautogui.press('tab')
    print("Tab key pressed.")
  except pyautogui.FailSafeException:
    print("PyAutoGUI fail-safe triggered. Move mouse to a corner of the screen to stop.")
  except Exception as e:
    print(f"An error occurred: {e}")


def delete_all(): 
  pyautogui.hotkey('ctrl', 'a')
  pyautogui.press('backspace')   

def save_file(file_name):
    pyautogui.hotkey("ctrl", "s")

def close_file():
    pyautogui.hotkey("alt", "f4")