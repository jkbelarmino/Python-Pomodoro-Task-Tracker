import tkinter as tk
from tkinter import ttk, messagebox
import json, time, threading, os, winsound

BASE_PATH = r"F:\Python Project\tasktracker"
TASKS_FILE = os.path.join(BASE_PATH, "tasks.json")

class TaskTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Tracker with Pomodoro")
        self.root.configure(bg="#1e1e1e")
        self.alert_active = False

        self.tasks = []
        self.timer_running = False
        self.remaining_time = 25 * 60
        self.selected_duration = 25 * 60
        self.selected_index = None

        self.build_gui()
        self.load_tasks()

    def build_gui(self):
        # Task Entry Frame
        entry_frame = tk.Frame(self.root, bg="#2e2e2e", width=200)
        entry_frame.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(entry_frame, text="New Task", fg="white", bg="#2e2e2e").pack()
        self.task_entry = tk.Entry(entry_frame, width=25)
        self.task_entry.pack(pady=5)

        tk.Label(entry_frame, text="Priority", fg="white", bg="#2e2e2e").pack()
        self.priority_var = tk.StringVar(value="Medium")
        ttk.Combobox(entry_frame, textvariable=self.priority_var, values=["High", "Medium", "Low"]).pack(pady=5)

        tk.Button(entry_frame, text="➕ Add Task", command=self.add_task).pack(pady=10)
        tk.Button(entry_frame, text="🗑️ Delete Task", command=self.delete_task).pack(pady=5)
        tk.Button(entry_frame, text="💾 Save Tasks", command=self.save_tasks).pack(pady=5)
        tk.Button(entry_frame, text="📂 Load Tasks", command=self.load_tasks).pack(pady=5)
        tk.Button(entry_frame, text="🧹 Clear Tasks", command=self.clear_all_tasks).pack(pady=5)
        tk.Button(entry_frame, text="🔼 Move Up", command=self.move_up).pack(pady=5)
        tk.Button(entry_frame, text="🔽 Move Down", command=self.move_down).pack(pady=5)

        # Task List Frame
        list_frame = tk.Frame(self.root, bg="#1e1e1e", width=400)
        list_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.task_display = tk.Text(list_frame, font=("Courier", 12), bg="#121212", fg="white", wrap="word")
        self.task_display.pack(fill="both", expand=True)
        self.task_display.config(state="disabled")

        self.task_display.tag_config("High", foreground="red")
        self.task_display.tag_config("Medium", foreground="orange")
        self.task_display.tag_config("Low", foreground="green", background="#cccccc")  # Improved readability
        self.task_display.tag_config("highlight", background="#444444")

        self.task_display.bind("<Button-1>", self.select_task)

        # Pomodoro Frame
        pomo_frame = tk.Frame(self.root, bg="#2e2e2e", width=200)
        pomo_frame.pack(side="right", fill="y", padx=10, pady=10)

        self.timer_label = tk.Label(pomo_frame, text="25:00", font=("Helvetica", 32), fg="white", bg="#2e2e2e")
        self.timer_label.pack(pady=20)

        self.progress = ttk.Progressbar(pomo_frame, length=200, mode="determinate")
        self.progress.pack(pady=10)

        duration_frame = tk.Frame(pomo_frame, bg="#2e2e2e")
        duration_frame.pack(pady=10)

        tk.Label(duration_frame, text="Choose Duration", fg="white", bg="#2e2e2e").pack()
        tk.Button(duration_frame, text="15 min", command=lambda: self.set_duration(15)).pack(side="left", padx=5)
        tk.Button(duration_frame, text="20 min", command=lambda: self.set_duration(20)).pack(side="left", padx=5)
        tk.Button(duration_frame, text="30 min", command=lambda: self.set_duration(30)).pack(side="left", padx=5)

        button_row = tk.Frame(pomo_frame, bg="#2e2e2e")
        button_row.pack(pady=10)

        tk.Button(button_row, text="Start Pomodoro", command=self.start_timer, width=12).pack(side="left", padx=5)
        tk.Button(button_row, text="Stop", command=self.stop_timer, width=12).pack(side="left", padx=5)

    def set_duration(self, minutes):
        self.selected_duration = minutes * 60
        self.remaining_time = self.selected_duration
        self.update_timer_display()

    def add_task(self):
        task = self.task_entry.get().strip()
        priority = self.priority_var.get()
        if task:
            self.tasks.append({"task": task, "priority": priority})
            self.refresh_task_display()
            self.task_entry.delete(0, "end")

    def delete_task(self):
        i = self.selected_index
        if i is not None and 0 <= i < len(self.tasks):
            task_text = self.tasks[i]["task"]
            confirm = messagebox.askyesno("Delete Task", f"Are you sure you want to delete:\n\n{task_text}")
            if confirm:
                self.tasks.pop(i)
                self.selected_index = None
                self.refresh_task_display()

    def save_tasks(self):
        try:
            with open(TASKS_FILE, "w") as f:
                json.dump(self.tasks, f, indent=2)
            messagebox.showinfo("Saved", "Tasks saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks:\n{e}")

    def load_tasks(self):
        try:
            if not os.path.exists(TASKS_FILE):
                with open(TASKS_FILE, "w") as f:
                    json.dump([], f)
            with open(TASKS_FILE, "r") as f:
                self.tasks = json.load(f)
            self.refresh_task_display()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tasks:\n{e}")

    def clear_all_tasks(self):
        self.tasks = []
        self.selected_index = None
        self.refresh_task_display()

    def refresh_task_display(self):
        self.task_display.config(state="normal")
        self.task_display.delete("1.0", "end")
        for i, t in enumerate(self.tasks):
            line = f"[{t['priority']}] {t['task']}\n"
            self.task_display.insert("end", line, t["priority"])
            if i == self.selected_index:
                line_start = f"{i + 1}.0"
                line_end = f"{i + 1}.end"
                self.task_display.tag_add("highlight", line_start, line_end)
        self.task_display.config(state="disabled")

    def select_task(self, event):
        index = int(self.task_display.index(f"@{event.x},{event.y}").split('.')[0]) - 1
        if 0 <= index < len(self.tasks):
            self.selected_index = index
            self.refresh_task_display()

    def move_up(self):
        i = self.selected_index
        if i is not None and i > 0:
            self.tasks[i], self.tasks[i - 1] = self.tasks[i - 1], self.tasks[i]
            self.selected_index -= 1
            self.refresh_task_display()

    def move_down(self):
        i = self.selected_index
        if i is not None and i < len(self.tasks) - 1:
            self.tasks[i], self.tasks[i + 1] = self.tasks[i + 1], self.tasks[i]
            self.selected_index += 1
            self.refresh_task_display()

    def start_timer(self):
        self.stop_alert()
        if not self.timer_running:
            self.remaining_time = self.selected_duration
            self.timer_running = True
            self.update_timer_display()
            self.highlight_first_task()
            threading.Thread(target=self.run_timer, daemon=True).start()

    def stop_timer(self):
        self.stop_alert()
        self.timer_running = False
        self.remaining_time = self.selected_duration
        self.update_timer_display()
        self.prompt_clear_first_task()

    def run_timer(self):
        while self.remaining_time > 0 and self.timer_running:
            time.sleep(1)
            self.remaining_time -= 1
            self.update_timer_display()
        if self.remaining_time == 0:
            self.timer_running = False
            threading.Thread(target=self.play_looping_alert, daemon=True).start()
            self.flash_screen()
            messagebox.showinfo("Pomodoro", "Time's up!")

    def update_timer_display(self):
        mins, secs = divmod(self.remaining_time, 60)
        self.timer_label.config(text=f"{mins:02}:{secs:02}")
        self.progress["value"] = ((self.selected_duration - self.remaining_time) / self.selected_duration) * 100

    def flash_screen(self):
        colors = ["#ff0000", "#00ff00", "#0000ff", "#ffff00", "#ff00ff"]
        for i in range(10):
            self.root.configure(bg=colors[i % len(colors)])
            self.root.update()
            time.sleep(0.2)
        self.root.configure(bg="#1e1e1e")  # Restore default background

    def play_looping_alert(self):
        self.alert_active = True
        while self.alert_active:
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            time.sleep(1)

    def stop_alert(self):
        self.alert_active = False
        winsound.PlaySound(None, winsound.SND_PURGE)

    def highlight_first_task(self):
        self.task_display.tag_remove("highlight", "1.0", "end")
        if self.tasks:
            self.task_display.tag_add("highlight", "1.0", "1.end")

    def prompt_clear_first_task(self):
        if self.tasks:
            response = messagebox.askyesno("Clear Task", "Clear the first task?")
            if response:
                self.tasks.pop(0)
                self.selected_index = None
                self.refresh_task_display()

if __name__ == "__main__":
    if not os.path.exists(BASE_PATH):
        os.makedirs(BASE_PATH)
    root = tk.Tk()
    root.state('zoomed')
    app = TaskTrackerApp(root)
    root.mainloop()

