import time
import tkinter as tk
from tkinter import messagebox

def show_alert():
    print("show alertttt")
    # Create a hidden Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Show an info messagebox
    messagebox.showinfo("Alert", "⏰ This is your pop-up alert!")

    root.destroy()  # Destroy the hidden window after alert


def countdown(minutes):
    seconds = minutes * 60
    while seconds >= 0:
        mins, secs = divmod(seconds, 60)
        print(f"\r⏳ {mins:02d}:{secs:02d}", end="", flush=True)
        time.sleep(1)
        seconds -= 1
    print("\n✅ Time's up!")
    # show_alert()

def main():
    while True:
        print("\n🍅 Pomodoro Timer")
        print("1. Start 25-minute Pomodoro")
        print("2. Start 5-minute Break")
        print("3. Start x-minute Break")
        print("4. Exit")
        choice = input("Select: ")

        if choice == '1':
            countdown(25)
        elif choice == '2':
            countdown(5)
        elif choice == '3':
            new_choice = input("Set x minute ")
            countdown(int(new_choice))
        elif choice == '4':
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
