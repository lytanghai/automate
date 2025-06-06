import pyautogui
import time
import random
import sys
import threading

def move_mouse():
    print("Starting mouse mover. Press Ctrl+C to stop.")
    while True:
        # Get current position
        x, y = pyautogui.position()
        # Move mouse slightly and back
        pyautogui.moveTo(x + 50, y + 65, duration=2)
        pyautogui.moveTo(x, y, duration=2)
        print("Mouse moved")
        time.sleep(5)

loading_done = False  # Flag to control logging thread

def print_mock_logs():
    logs = [
        "Connecting to server...",
        "Fetching data...",
        "Parsing response...",
        "Validating schema...",
        "Checking dependencies...",
        "Initializing modules...",
        "Finalizing setup...",
        "Cleaning temporary files...",
        "Almost done..."
    ]
    while not loading_done:
        print(f"\n{random.choice(logs)}")
        time.sleep(1.5)


def print_progress_bar():
    global loading_done
    for i in range(1, 101):
        bar_length = 50
        filled_length = int(bar_length * i // 100)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        sys.stdout.write(f'\rLoading |{bar}| {i}%')
        sys.stdout.flush()
        time.sleep(0.05)
    loading_done = True
    print("\n✅ Loading Complete!")


def main():
    log_thread = threading.Thread(target=print_mock_logs)
    log_thread.start()

    print_progress_bar()

    log_thread.join()  # Wait for log thread to finish

if __name__ == "__main__":
    try:
        # move_mouse()
        while True:
            # main()
            move_mouse()
    except KeyboardInterrupt:
        print("\nStopped by user.")
