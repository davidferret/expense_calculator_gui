import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def init_db():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        amount REAL,
                        category TEXT,
                        description TEXT,
                        date TEXT)''')
    conn.commit()
    conn.close()

def add_expense():
    amount = amount_entry.get()
    category = category_var.get()
    description = description_entry.get()
    date = date_entry.get()
    
    if not amount or not category or not date:
        messagebox.showerror("Error", "All fields except description are required!")
        return
    
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number!")
        return
    
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)", 
                   (amount, category, description, date))
    conn.commit()
    conn.close()
    
    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    load_expenses()
    messagebox.showinfo("Success", "Expense added successfully!")

def load_expenses():
    for row in expense_tree.get_children():
        expense_tree.delete(row)
    
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, amount, category, description, date FROM expenses")
    rows = cursor.fetchall()
    conn.close()
    
    for row in rows:
        expense_tree.insert("", tk.END, values=row)

root = tk.Tk()
root.title("Expense Tracker")
root.geometry("600x400")

frame = ttk.Frame(root)
frame.pack(pady=10)

amount_label = ttk.Label(frame, text="Amount:")
amount_label.grid(row=0, column=0, padx=5, pady=5)
amount_entry = ttk.Entry(frame)
amount_entry.grid(row=0, column=1, padx=5, pady=5)

category_label = ttk.Label(frame, text="Category:")
category_label.grid(row=0, column=2, padx=5, pady=5)
category_var = tk.StringVar()
category_dropdown = ttk.Combobox(frame, textvariable=category_var, values=["Food", "Transport", "Entertainment", "Other"])
category_dropdown.grid(row=0, column=3, padx=5, pady=5)
category_dropdown.current(0)

description_label = ttk.Label(frame, text="Description:")
description_label.grid(row=1, column=0, padx=5, pady=5)
description_entry = ttk.Entry(frame)
description_entry.grid(row=1, column=1, padx=5, pady=5)

date_label = ttk.Label(frame, text="Date (YYYY-MM-DD):")
date_label.grid(row=1, column=2, padx=5, pady=5)
date_entry = ttk.Entry(frame)
date_entry.grid(row=1, column=3, padx=5, pady=5)

add_button = ttk.Button(root, text="Add Expense", command=add_expense)
add_button.pack(pady=5)

columns = ("ID", "Amount", "Category", "Description", "Date")
expense_tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    expense_tree.heading(col, text=col)
    expense_tree.column(col, width=100)
expense_tree.pack(pady=10)

init_db()
load_expenses()

root.mainloop()
