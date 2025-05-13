import sys
import time
import threading

loading_active = False
loading_thread = None

def loading():
    global loading_active, loading_thread

    def animate():
        i = 0
        while loading_active:
            sys.stdout.write(f'\rLoading... {i}%')
            sys.stdout.flush()
            i = (i + 1) if i < 99 else 99
            time.sleep(0.05)

    loading_active = True
    loading_thread = threading.Thread(target=animate)
    loading_thread.start()

def end_loading():
    global loading_active, loading_thread
    loading_active = False
    loading_thread.join()
    sys.stdout.write('\rLoading... 100%\n')
    sys.stdout.flush()
    time.sleep(1)

# Example usage
def update_user_profile():
    print("\nUpdating user profile...\n")
    time.sleep(1)  # Simulate update work
    print("User profile updated.")

if __name__ == "__main__":
    loading()
    update_user_profile()
    end_loading()
