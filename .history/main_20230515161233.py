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
    update_expense_history()
    update_balance()

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

def update_expense_history():
    cursor.execute(
        """
        SELECT name, amount, date FROM expenses ORDER BY date DESC LIMIT 5
        """
    )
    data = cursor.fetchall()

    history_text = ""
    for row in data:
        name = row[0]
        amount = row[1]
        date = row[2]
        history_text += f"{date} - {name}: ${amount}\n"

    text_expense_history.config(state=tk.NORMAL)
    text_expense_history.delete("1.0", tk.END)
    text_expense_history.insert(tk.END, history_text)
    text_expense_history.config(state=tk.DISABLED)

def update_balance():
    cursor.execute(
        """
        SELECT SUM(amount) FROM expenses
        """
    )
    balance = cursor.fetchone()[0]
    if balance:
        label_balance.config(text=f"Current Balance: ${balance}")
    else:
        label_balance.config(text="Current Balance: $0")

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

button_add = tk.Button(window,text="Add Expense", command=add_expense)
button_add.pack()

label_balance = tk.Label(window, text="Current Balance: $0")
label_balance.pack()

label_expense_history = tk.Label(window, text="Expense History:")
label_expense_history.pack()

text_expense_history = tk.Text(window, height=5, width=30)
text_expense_history.pack()
text_expense_history.config(state=tk.DISABLED)

button_chart = tk.Button(window, text="Show Expense Chart", command=update_chart)
button_chart.pack()

Update initial balance and expense history
update_balance()
update_expense_history()

window.mainloop()

connection.close()