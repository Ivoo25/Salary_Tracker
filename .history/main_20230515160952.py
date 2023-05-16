import tkinter as tk
from datetime import date
import sqlite3
import matplotlib.pyplot as plt
from tkinter import messagebox
from tkinter import ttk

def add_expense():
    name = combo_category.get()
    amount = entry_amount.get()
    today = date.today()
    cursor.execute(
        """
        INSERT INTO expenses (name, amount, date) VALUES (?, ?, ?)
        """,
        (name, amount, today)
    )
    connection.commit()
    entry_amount.delete(0, tk.END)
    update_chart()

def update_chart():
    cursor.execute(
        """
        SELECT name, SUM(amount) FROM expenses GROUP BY name
        """
    )
    data = cursor.fetchall()

    categories = []
    amounts = []
    for row in data:
        categories.append(row[0])
        amounts.append(row[1])

    plt.figure(figsize=(8, 6))
    plt.bar(categories, amounts)
    plt.xlabel("Categories")
    plt.ylabel("Amount")
    plt.title("Expense Distribution")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def add_new_category():
    new_category = entry_new_category.get()
    if new_category.strip() == "":
        messagebox.showerror("Error", "Please enter a category name.")
        return
    combo_category["values"] = list(combo_category["values"]) + [new_category]
    combo_category.current(len(combo_category["values"]) - 1)
    entry_new_category.delete(0, tk.END)

window = tk.Tk()
window.title("Salary Tracker")

connection = sqlite3.connect("salary_tracker.db")
cursor = connection.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        amount INTEGER,
        date DATE
    )
    """
)
connection.commit()

label_category = tk.Label(window, text="Expense Category:")
label_category.pack()
combo_category = ttk.Combobox(window, values=["Department's rent", "Department's cleaning stuff", "Food", "Gym", "Eating Out", "Health"])
combo_category.pack()

label_new_category = tk.Label(window, text="New Category:")
label_new_category.pack()
entry_new_category = tk.Entry(window)
entry_new_category.pack()

button_new_category = tk.Button(window, text="Add New Category", command=add_new_category)
button_new_category.pack()

label_amount = tk.Label(window, text="Expense Amount:")
label_amount.pack()
entry_amount = tk.Entry(window)
entry_amount.pack()

button_add = tk.Button(window, text="Add Expense", command=add_expense)
button_add.pack()

button_chart = tk.Button(window, text="Show Expense Chart", command=update_chart)
button_chart.pack()

window.mainloop()

connection.close()
