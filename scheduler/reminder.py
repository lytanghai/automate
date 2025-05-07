import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog
from tkcalendar import DateEntry
from plyer import notification
import schedule
import threading
import time
import json
import datetime
import os

TASK_FILE = "scheduler/tasks.json"

class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Scheduler")
        self.tasks = []

        self.create_widgets()
        self.load_tasks()
        self.start_scheduler_thread()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="Task Description").grid(row=0, column=0)
        self.task_entry = tk.Entry(frame, width=30)
        self.task_entry.grid(row=0, column=1, columnspan=2)

        tk.Label(frame, text="Type").grid(row=1, column=0)
        self.type_var = tk.StringVar()
        self.type_cb = ttk.Combobox(frame, textvariable=self.type_var, values=["Today", "Everyday", "Tomorrow", "Select Date"])
        self.type_cb.grid(row=1, column=1)
        self.type_cb.bind("<<ComboboxSelected>>", self.toggle_date_picker)

        self.date_picker = DateEntry(frame)
        self.date_picker.grid(row=1, column=2)
        self.date_picker.grid_remove()

        tk.Label(frame, text="Schedule").grid(row=2, column=0)
        self.schedule_var = tk.StringVar()
        self.schedule_cb = ttk.Combobox(frame, textvariable=self.schedule_var,
                                        values=["Every Minute", "Every X Minutes", "Every Hour", "At Time"])
        self.schedule_cb.grid(row=2, column=1)
        self.schedule_cb.bind("<<ComboboxSelected>>", self.toggle_time_input)

        self.time_input = tk.Entry(frame)
        self.time_input.grid(row=2, column=2)
        self.time_input.grid_remove()

        tk.Button(frame, text="Add Task", command=self.add_task).grid(row=3, column=0, columnspan=3, pady=5)

        self.task_listbox = tk.Listbox(frame, width=60)
        self.task_listbox.grid(row=4, column=0, columnspan=3, pady=10)

        tk.Button(frame, text="Delete Selected Task", command=self.delete_task).grid(row=5, column=0, columnspan=3)

    def toggle_date_picker(self, event):
        if self.type_var.get() == "Select Date":
            self.date_picker.grid()
        else:
            self.date_picker.grid_remove()

    def toggle_time_input(self, event):
        selected = self.schedule_var.get()
        if selected in ["Every X Minutes", "At Time"]:
            self.time_input.grid()
        else:
            self.time_input.grid_remove()

    def add_task(self):
        desc = self.task_entry.get()
        task_type = self.type_var.get()
        schedule_type = self.schedule_var.get()
        time_value = self.time_input.get()

        print(f"schedule type {schedule_type}")
        if not desc or not task_type or not schedule_type:
            messagebox.showerror("Error", "All fields are required.")
            return

        if task_type == "Select Date":
            task_date = self.date_picker.get_date().strftime("%Y-%m-%d")
        else:
            task_date = task_type

        task = {
            "description": desc,
            "type": task_type,
            "date": task_date,
            "schedule": schedule_type,
            "time": time_value
        }
        schedule_type = schedule_type.replace("X", time_value)
        self.tasks.append(task)
        self.task_listbox.insert(tk.END, f"{desc} - {task_type} - {schedule_type}")
        self.save_tasks()
        self.schedule_task(task)

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if not selected:
            return
        index = selected[0]
        self.tasks.pop(index)
        self.task_listbox.delete(index)
        self.save_tasks()

    def show_notification(self, title, message):
        notification.notify(
            title=title,
            message=message,
            timeout=10
        )

    def schedule_task(self, task):
        def job():
            now = datetime.datetime.now().strftime("%Y-%m-%d")
            if task["type"] == "Today" and now == datetime.date.today().strftime("%Y-%m-%d"):
                self.show_notification("Reminder", task["description"])
            elif task["type"] == "Tomorrow":
                tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
                if now == tomorrow:
                    self.show_notification("Reminder", task["description"])
            elif task["type"] == "Everyday":
                self.show_notification("Reminder", task["description"])
            elif task["type"] == "Select Date" and now == task["date"]:
                self.show_notification("Reminder", task["description"])

        if task["schedule"] == "Every X Minute":
            schedule.every(1).minutes.do(job)
        elif task["schedule"] == "Every Minutes":
            try:
                interval = int(task["time"])
                schedule.every(interval).minutes.do(job)
            except ValueError:
                messagebox.showerror("Error", "Invalid number for X minutes")
        elif task["schedule"] == "Every Hour":
            schedule.every().hour.do(job)
        elif task["schedule"] == "At Time":
            schedule.every().day.at(task["time"]).do(job)

    def start_scheduler_thread(self):
        def run():
            while True:
                schedule.run_pending()
                time.sleep(1)

        t = threading.Thread(target=run, daemon=True)
        t.start()

    def save_tasks(self):
        with open(TASK_FILE, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def load_tasks(self):
        if os.path.exists(TASK_FILE):
            with open(TASK_FILE, "r") as f:
                self.tasks = json.load(f)
                for task in self.tasks:
                    self.task_listbox.insert(tk.END, f"{task['description']} - {task['type']} - {task['schedule']} {task['time']}")
                    self.schedule_task(task)

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()
