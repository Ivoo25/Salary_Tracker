import tkinter as tk
from datetime import date
import sqlite3

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

window.mainloop()

connection.close()
