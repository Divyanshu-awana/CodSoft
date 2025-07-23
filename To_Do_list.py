import tkinter as tk
from tkinter import simpledialog, messagebox, Menu
import json
import os

DATA_FILE = 'tasks.json'
# Loads the File
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}
# Save the File
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Task Manager")
        self.task_lists = load_data()

        # Frames
        frame_left = tk.Frame(root)
        frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        frame_right = tk.Frame(root)
        frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Listbox for task lists (left)
        tk.Label(frame_left, text="Task Lists").pack()
        self.listbox_lists = tk.Listbox(frame_left, width=25, exportselection=False)
        self.listbox_lists.pack(fill=tk.Y, expand=True)
        self.listbox_lists.bind("<<ListboxSelect>>", self.on_list_select)

        button_frame = tk.Frame(frame_left)
        button_frame.pack(pady=5)
        tk.Button(button_frame, text="Add List", command=self.add_list).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Delete List", command=self.delete_list).pack(side=tk.LEFT)

        # Listbox for tasks (right)
        tk.Label(frame_right, text="Tasks").pack()
        self.listbox_tasks = tk.Listbox(frame_right, width=50, exportselection=False)
        self.listbox_tasks.pack(fill=tk.BOTH, expand=True)
        self.listbox_tasks.bind('<Button-1>', self.on_task_left_click)
        self.listbox_tasks.bind('<Button-3>', self.show_task_menu)  # Right-click (Windows/Linux)
        self.listbox_tasks.bind('<Button-2>', self.show_task_menu)  # Right-click (macOS)

        task_btn_frame = tk.Frame(frame_right)
        task_btn_frame.pack(pady=5)
        tk.Button(task_btn_frame, text="Add Task", command=self.add_task).pack(side=tk.LEFT)
        tk.Button(task_btn_frame, text="Edit Task", command=self.edit_task).pack(side=tk.LEFT)
        tk.Button(task_btn_frame, text="Delete Task", command=self.delete_task).pack(side=tk.LEFT)
        tk.Button(task_btn_frame, text="Mark Complete/Incomplete", command=self.toggle_task_complete).pack(side=tk.LEFT)

        # Context menu for tasks
        self.task_menu = Menu(self.root, tearoff=0)
        self.task_menu.add_command(label="Edit Task", command=self.edit_task)
        self.task_menu.add_command(label="Delete Task", command=self.delete_task)
        self.task_menu.add_command(label="Mark Complete/Incomplete", command=self.toggle_task_complete)

        self.refresh_lists()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def refresh_lists(self):
        self.listbox_lists.delete(0, tk.END)
        for list_name in self.task_lists:
            self.listbox_lists.insert(tk.END, list_name)
        self.refresh_tasks(clear_selection=True)

    def refresh_tasks(self, clear_selection=False):
        selection = self.listbox_lists.curselection()
        old_task_selection = self.listbox_tasks.curselection()
        self.listbox_tasks.delete(0, tk.END)
        if selection:
            list_name = self.listbox_lists.get(selection[0])
            tasks = self.task_lists.get(list_name, [])
            for idx, task in enumerate(tasks):
                display = ('✅ ' if task.get('done') else '⬜ ') + task['text']
                self.listbox_tasks.insert(tk.END, display)
            # Reselect task if possible, unless clearing selection
            if (not clear_selection) and old_task_selection and 0 <= old_task_selection[0] < len(tasks):
                self.listbox_tasks.select_set(old_task_selection[0])

    def on_list_select(self, event):
        self.refresh_tasks(clear_selection=True)

    def on_task_left_click(self, event):
        # Robust selection: select the task under the pointer only, do not affect lists
        idx = self.listbox_tasks.nearest(event.y)
        self.listbox_tasks.select_clear(0, tk.END)
        self.listbox_tasks.select_set(idx)
        self.listbox_tasks.activate(idx)
        # Prevent event propagation to frame/parent (fixes selection bug!)
        return 'break'

    def add_list(self):
        list_name = simpledialog.askstring("Add List", "Enter list name:")
        if list_name:
            if list_name in self.task_lists:
                messagebox.showerror("Error", "List already exists.")
            else:
                self.task_lists[list_name] = []
                self.refresh_lists()

    def delete_list(self):
        selection = self.listbox_lists.curselection()
        if not selection:
            messagebox.showerror("Error", "Select a list to delete.")
            return
        list_name = self.listbox_lists.get(selection[0])
        confirm = messagebox.askyesno("Confirm", f"Delete list '{list_name}' and all its tasks?")
        if confirm:
            del self.task_lists[list_name]
            self.refresh_lists()

    def add_task(self):
        selection = self.listbox_lists.curselection()
        if not selection:
            messagebox.showerror("Error", "Select a list first.")
            return
        list_name = self.listbox_lists.get(selection[0])
        task_text = simpledialog.askstring("Add Task", f"Task for '{list_name}':")
        if task_text:
            self.task_lists[list_name].append({'text': task_text, 'done': False})
            self.refresh_tasks()

    def delete_task(self):
        lsel = self.listbox_lists.curselection()
        tsel = self.listbox_tasks.curselection()
        if not (lsel and tsel):
            messagebox.showerror("Error", "Select a task to delete.")
            return
        list_name = self.listbox_lists.get(lsel[0])
        idx = tsel[0]
        task_text = self.task_lists[list_name][idx]['text']
        confirm = messagebox.askyesno("Confirm", f"Delete this task: '{task_text}'?")
        if confirm:
            del self.task_lists[list_name][idx]
            self.refresh_tasks()

    def edit_task(self):
        lsel = self.listbox_lists.curselection()
        tsel = self.listbox_tasks.curselection()
        if not (lsel and tsel):
            messagebox.showerror("Error", "Select a task to edit.")
            return
        list_name = self.listbox_lists.get(lsel[0])
        idx = tsel[0]
        old_text = self.task_lists[list_name][idx]['text']
        new_text = simpledialog.askstring("Edit Task", "Edit task text:", initialvalue=old_text)
        if new_text:
            self.task_lists[list_name][idx]['text'] = new_text
            self.refresh_tasks()

    def toggle_task_complete(self):
        lsel = self.listbox_lists.curselection()
        tsel = self.listbox_tasks.curselection()
        if not (lsel and tsel):
            messagebox.showerror("Error", "Select a task to mark.")
            return
        list_name = self.listbox_lists.get(lsel[0])
        idx = tsel[0]
        task = self.task_lists[list_name][idx]
        task['done'] = not task.get('done', False)
        self.refresh_tasks()

    def show_task_menu(self, event):
        idx = self.listbox_tasks.nearest(event.y)
        self.listbox_tasks.select_clear(0, tk.END)
        self.listbox_tasks.select_set(idx)
        self.listbox_tasks.activate(idx)
        try:
            self.task_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.task_menu.grab_release()
        return 'break'  # Prevent event propagation (important)

    def on_closing(self):
        save_data(self.task_lists)
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()
