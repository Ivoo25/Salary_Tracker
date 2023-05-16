import tkinter as tk
from datetime import date
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

def add_expense():
    name = entry_name.get()
    amount = entry_amount.get()
    today = date.today()
    cursor.execute(
        """
        INSERT INTO expenses (name, amount, date) VALUES (?, ?, ?)
        """,
        (name, amount, today)
    )
    connection.commit()
    entry_name.delete(0, tk.END)
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

def add_salary():
    cursor.execute(
        """
        DELETE FROM expenses
        """
    )
    salary = entry_salary.get()
    today = date.today()
    cursor.execute(
        """
        INSERT INTO expenses (name, amount, date) VALUES (?, ?, ?)
        """,
        ("Salary", salary, today)
    )
    connection.commit()
    entry_salary.delete(0, tk.END)
    update_chart()

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

label_name = tk.Label(window, text="Expense Name:")
label_name.pack()
entry_name = tk.Entry(window)
entry_name.pack()

label_amount = tk.Label(window, text="Expense Amount:")
label_amount.pack()
entry_amount = tk.Entry(window)
entry_amount.pack()

button_add = tk.Button(window, text="Add Expense", command=add_expense)
button_add.pack()

label_salary = tk.Label(window, text="Input Salary:")
label_salary.pack()
entry_salary = tk.Entry(window)
entry_salary.pack()

button_salary = tk.Button(window, text="Add Salary", command=add_salary)
button_salary.pack()

button_chart = tk.Button(window, text="Show Expense Chart", command=update_chart)
button_chart.pack()

window.mainloop()

connection.close()
