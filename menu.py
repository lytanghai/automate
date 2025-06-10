import tkinter as tk
from datetime import datetime
import subprocess
import sys

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tool")
        self.geometry("900x550")
        self.configure(bg="#1e1b2e")

        # Top bar with tool name and datetime + interval
        top_frame = tk.Frame(self, bg="#1e1b2e")
        top_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        tk.Label(top_frame, text="Tool", fg="white", bg="#1e1b2e", font=("Arial", 14, "bold")).pack(side=tk.LEFT)

        datetime_frame = tk.Frame(top_frame, bg="#1e1b2e")
        datetime_frame.pack(side=tk.RIGHT)

        # Live-updating current datetime
        tk.Label(datetime_frame, text="Date:", fg="white", bg="#1e1b2e").grid(row=0, column=0, padx=5)
        self.date_entry = tk.Entry(datetime_frame, width=20)
        self.date_entry.grid(row=0, column=1)   
        self.update_datetime()  # Start updating


        # Menu buttons
        menu_frame = tk.Frame(self, bg="#1e1b2e")
        menu_frame.pack(pady=20)

        self.menu_buttons = [
            ("NETWORK", self.open_network),
            ("FILE", self.open_file),
            ("AUTOMATION", self.open_automation),
            ("CREDENTIAL", self.open_credential),
            ("QUICK_ACCESS", self.open_quick_access),
            ("SETTINGS", self.open_settings),
            ("LOGGING", self.open_logging),
            ("HELP", self.open_help),
            ("UPDATE", self.open_update),
            ("ABOUT", self.open_about),
        ]
        self.render_buttons(menu_frame)

    def update_datetime(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, now)
        self.after(1000, self.update_datetime)  # update every second

    def render_buttons(self, parent):
        for i, (label, command) in enumerate(self.menu_buttons):
            row = i // 5
            col = i % 5
            tk.Button(
                parent, text=label, width=15, height=4,
                bg="#1e1b2e", fg="white", highlightbackground="white",
                command=command
            ).grid(row=row, column=col, padx=10, pady=10)

    def open_network(self): self.redirect("network/network.py")
    def open_file(self): self.redirect("file")
    def open_automation(self): self.redirect("automation")
    def open_credential(self): self.redirect("credential")
    def open_quick_access(self): self.redirect("quick_access")
    def open_settings(self): self.redirect("settings")
    def open_logging(self): self.redirect("logging")
    def open_help(self): self.redirect("help")
    def open_update(self): self.redirect("update")
    def open_about(self): self.redirect("about")

    def redirect(self, menu_name):
        print(f"Redirecting to {menu_name}.py")
        subprocess.Popen([sys.executable, menu_name])
        self.destroy()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
