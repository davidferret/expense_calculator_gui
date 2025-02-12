import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
from datetime import date
import matplotlib.pyplot as plt

# database
def execute_query(query, params=(), fetch=False):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    data = cursor.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return data

def init_db():
    execute_query('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        amount REAL,
                        category TEXT,
                        description TEXT,
                        date TEXT)''')

def add_expense():
    try:
        amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number!")
        return
    if not category_var.get() or not date_entry.get():
        messagebox.showerror("Error", "All fields except description are required!")
        return
    execute_query("INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
                  (amount, category_var.get(), description_entry.get(), date_entry.get()))
    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    date_entry.set_date(date.today())
    load_expenses()
    messagebox.showinfo("Success", "Expense added successfully!")

def update_total_spending():
    rows = execute_query("SELECT category, SUM(amount) FROM expenses GROUP BY category", fetch=True)
    total_text.set("Total Spending Per Category:\n" + "\n".join([f"{r[0]}: ${r[1]:.2f}" for r in rows]))

def load_expenses():
    for row in expense_tree.get_children():
        expense_tree.delete(row)
    query = "SELECT id, amount, category, description, date FROM expenses WHERE 1=1"
    params = []
    if filter_category_var.get() != "All":
        query += " AND category=?"
        params.append(filter_category_var.get())
    if start_date_entry.get() and end_date_entry.get():
        query += " AND date BETWEEN ? AND ?"
        params.extend([start_date_entry.get(), end_date_entry.get()])
    rows = execute_query(query, params, fetch=True)
    for row in rows:
        expense_tree.insert("", tk.END, values=(row[0], f"${row[1]:.2f}", row[2], row[3], row[4]))
    update_total_spending()

def show_pie_chart():
    rows = execute_query("SELECT category, SUM(amount) FROM expenses GROUP BY category", fetch=True)
    if not rows:
        messagebox.showinfo("No Data", "No expenses available for visualization.")
        return
    categories, amounts = zip(*rows)
    plt.figure(figsize=(6,6))
    plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=140)
    plt.title("Expense Distribution by Category")
    plt.show()

# gui
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("700x600")

frame = ttk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Amount:").grid(row=0, column=0, padx=5, pady=5)
amount_entry = ttk.Entry(frame)
amount_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Category:").grid(row=0, column=2, padx=5, pady=5)
category_var = tk.StringVar()
category_dropdown = ttk.Combobox(frame, textvariable=category_var, values=["Food", "Transport", "Entertainment", "Utilities", "Healthcare", "Shopping", "Travel", "Education", "Other"])
category_dropdown.grid(row=0, column=3, padx=5, pady=5)
category_dropdown.current(0)

tk.Label(frame, text="Description:").grid(row=1, column=0, padx=5, pady=5)
description_entry = ttk.Entry(frame)
description_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Date:").grid(row=1, column=2, padx=5, pady=5)
date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2, year=date.today().year, month=date.today().month, day=date.today().day)
date_entry.grid(row=1, column=3, padx=5, pady=5)

ttk.Button(root, text="Add Expense", command=add_expense).pack(pady=5)

filter_frame = ttk.Frame(root)
filter_frame.pack(pady=10)
filter_category_var = tk.StringVar()
filter_category_dropdown = ttk.Combobox(filter_frame, textvariable=filter_category_var, values=["All", "Food", "Transport", "Entertainment", "Utilities", "Healthcare", "Shopping", "Travel", "Education", "Other"])
filter_category_dropdown.grid(row=0, column=0, padx=5, pady=5)
filter_category_dropdown.current(0)
start_date_entry = DateEntry(filter_frame, width=12)
start_date_entry.grid(row=0, column=1, padx=5, pady=5)
end_date_entry = DateEntry(filter_frame, width=12)
end_date_entry.grid(row=0, column=2, padx=5, pady=5)
ttk.Button(filter_frame, text="Filter", command=load_expenses).grid(row=0, column=3, padx=5, pady=5)

columns = ("ID", "Amount", "Category", "Description", "Date")
expense_tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    expense_tree.heading(col, text=col)
    expense_tree.column(col, width=100)
expense_tree.pack(pady=10)

total_text = tk.StringVar()
ttk.Label(root, textvariable=total_text).pack(pady=5)
ttk.Button(root, text="Show Expense Chart", command=show_pie_chart).pack(pady=5)

init_db()
load_expenses()
root.mainloop()
