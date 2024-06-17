import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

# Initialize database
def init_db():
    conn = sqlite3.connect('todo_list.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            description TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            category TEXT,
            due_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Define functions to manage tasks
def add_task(description, priority, status, category, due_date):
    conn = sqlite3.connect('todo_list.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (description, priority, status, category, due_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (description, priority, status, category, due_date))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect('todo_list.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id=?', (task_id,))
    conn.commit()
    conn.close()

def update_task(task_id, description, priority, status, category, due_date):
    conn = sqlite3.connect('todo_list.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tasks
        SET description=?, priority=?, status=?, category=?, due_date=?
        WHERE id=?
    ''', (description, priority, status, category, due_date, task_id))
    conn.commit()
    conn.close()

def view_tasks(filter_by=None):
    conn = sqlite3.connect('todo_list.db')
    cursor = conn.cursor()
    query = 'SELECT * FROM tasks'
    if filter_by:
        query += ' WHERE ' + filter_by
    cursor.execute(query)
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# Define the GUI
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.root, columns=('ID', 'Description', 'Priority', 'Status', 'Category', 'Due Date'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Description', text='Description')
        self.tree.heading('Priority', text='Priority')
        self.tree.heading('Status', text='Status')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Due Date', text='Due Date')
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.refresh_tree()

        self.add_frame = ttk.Frame(self.root)
        self.add_frame.pack(fill=tk.X)

        self.desc_label = ttk.Label(self.add_frame, text="Description:")
        self.desc_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.desc_entry = ttk.Entry(self.add_frame)
        self.desc_entry.pack(side=tk.LEFT, padx=5, pady=5)

        self.priority_label = ttk.Label(self.add_frame, text="Priority:")
        self.priority_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.priority_entry = ttk.Entry(self.add_frame)
        self.priority_entry.pack(side=tk.LEFT, padx=5, pady=5)

        self.status_label = ttk.Label(self.add_frame, text="Status:")
        self.status_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.status_entry = ttk.Entry(self.add_frame)
        self.status_entry.pack(side=tk.LEFT, padx=5, pady=5)

        self.category_label = ttk.Label(self.add_frame, text="Category:")
        self.category_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.category_entry = ttk.Entry(self.add_frame)
        self.category_entry.pack(side=tk.LEFT, padx=5, pady=5)

        self.due_date_label = ttk.Label(self.add_frame, text="Due Date (YYYY-MM-DD):")
        self.due_date_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.due_date_entry = ttk.Entry(self.add_frame)
        self.due_date_entry.pack(side=tk.LEFT, padx=5, pady=5)

        self.add_button = ttk.Button(self.add_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.update_button = ttk.Button(self.add_frame, text="Update Task", command=self.update_task)
        self.update_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_button = ttk.Button(self.add_frame, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

    def refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        tasks = view_tasks()
        for task in tasks:
            self.tree.insert('', tk.END, values=task)

    def add_task(self):
        description = self.desc_entry.get()
        priority = self.priority_entry.get()
        status = self.status_entry.get()
        category = self.category_entry.get()
        due_date = self.due_date_entry.get()
        if description and priority and status:
            add_task(description, priority, status, category, due_date)
            self.refresh_tree()
        else:
            messagebox.showerror("Input Error", "Description, Priority, and Status are required fields.")

    def update_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "No task selected.")
            return
        task_id = self.tree.item(selected_item)['values'][0]
        description = self.desc_entry.get()
        priority = self.priority_entry.get()
        status = self.status_entry.get()
        category = self.category_entry.get()
        due_date = self.due_date_entry.get()
        if description and priority and status:
            update_task(task_id, description, priority, status, category, due_date)
            self.refresh_tree()
        else:
            messagebox.showerror("Input Error", "Description, Priority, and Status are required fields.")

    def delete_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "No task selected.")
            return
        task_id = self.tree.item(selected_item)['values'][0]
        delete_task(task_id)
        self.refresh_tree()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()

