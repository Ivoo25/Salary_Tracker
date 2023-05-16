import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import date, datetime
import numpy as np
import sqlite3
import matplotlib.pyplot as plt


# Define the default expense categories
expense_names = [
    "Department's rent",
    "Home stuff",
    "Food",
    "Gym",
    "Eating Out",
    "Health"
]

# Create the main window
window = tk.Tk()
window.title("Salary Tracker")
window.geometry("600x600")
window.config(padx=20, pady=20)


# Connect to the database
connection = sqlite3.connect("expenses.db")
cursor = connection.cursor()


# Create the expenses table if it doesn't exist
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        amount REAL,
        details TEXT,
        date TEXT
    )
    """
)
connection.commit()


# Function to update the balance label
def update_balance():
    # Get the last salary entry
    cursor.execute("SELECT amount FROM expenses WHERE name='Salary' ORDER BY date DESC LIMIT 1")
    last_salary = cursor.fetchone()
    
    if last_salary:
        last_salary_date_str = cursor.execute("SELECT date FROM expenses WHERE name='Salary' ORDER BY date DESC LIMIT 1").fetchone()
        last_salary_date = datetime.strptime(last_salary_date_str[0], "%Y-%m-%d").date()
        today = date.today()
        if last_salary_date.month == today.month and today.day != 1:
            # If the last salary is for the current month and it's not the first of the month, use the last salary amount
            balance = last_salary[0] - get_total_expenses()
        else:
            # If it's the first of the month or there is no last salary, prompt the user for the salary
            salary = prompt_salary()
            if salary is None:
                # If the user cancels the prompt, set the balance as N/A
                balance = "N/A"
            else:
                # Insert the new salary entry into the database
                cursor.execute("INSERT INTO expenses (name, amount, date) VALUES (?, ?, ?)", ("Salary", salary, today))
                connection.commit()
                balance = salary - get_total_expenses()
    else:
        # If there are no salary entries, prompt the user for the salary
        salary = prompt_salary()
        if salary is None:
            # If the user cancels the prompt, set the balance as N/A
            balance = "N/A"
        else:
            # Insert the new salary entry into the database
            cursor.execute("INSERT INTO expenses (name, amount, date) VALUES (?, ?, ?)", ("Salary", salary, date.today()))
            connection.commit()
            balance = salary - get_total_expenses()
    
    label_balance.config(text=f"Current Balance: ${balance:.2f}" if isinstance(balance, float) else f"Current Balance: {balance}")


# Function to prompt the user for the salary
def prompt_salary():
    return simpledialog.askfloat("Add Salary", "Enter your salary:")


# Function to get the total expenses
def get_total_expenses():
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE name!='Salary'")
    total_expenses = cursor.fetchone()[0] or 0
    return total_expenses


# Function to update the expense history
def update_expense_history():
    cursor.execute("SELECT name, amount, details, date FROM expenses WHERE name!='Salary' ORDER BY date DESC LIMIT 5")
    expenses = cursor.fetchall()
    text_expense_history.config(state=tk.NORMAL)
    text_expense_history.delete("1.0", tk.END)
    for expense in expenses:
        name, amount, details, date_str = expense
        text_expense_history.insert(tk.END, f"{date_str} - {name}: ${amount:.2f}\nDetails: {details}\n")
    text_expense_history.config(state=tk.DISABLED)




# Function to add an expense
def add_expense():
    name = combo_expense.get()
    amount = simpledialog.askfloat("Add Expense", f"How much did you spend on {name}?")
    if amount is not None:
        details = simpledialog.askstring("Expense Details", "Enter the details of your expense:")
        today = date.today()
        cursor.execute("INSERT INTO expenses (name, amount, details, date) VALUES (?, ?, ?, ?)",
                       (name, amount, details, today))
        connection.commit()
        update_balance()
        update_expense_history()



# Function to reset the app and erase all data
def reset_app():
    result = messagebox.askyesno("Reset Confirmation", "Are you sure you want to reset the app? This will erase all data.")
    if result:
        # Delete all data from the expenses table
        cursor.execute("DELETE FROM expenses")
        connection.commit()
        
        # Update the balance and expense history
        update_balance()
        update_expense_history()
        messagebox.showinfo("Reset", "The app has been reset.")


# Function to plot the expense breakdown
def plot_expense_breakdown():
    cursor.execute("SELECT name, SUM(amount) FROM expenses WHERE name!='Salary' GROUP BY name")
    expense_breakdown = cursor.fetchall()
    categories = [expense[0] for expense in expense_breakdown]
    amounts = [expense[1] for expense in expense_breakdown]

    fig, ax = plt.subplots()
    ax.bar(categories, amounts)
    ax.set_xlabel('Expense Categories')
    ax.set_ylabel('Amount')
    ax.set_title('Expense Breakdown')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# Function to plot the expense breakdown using a pie chart
def plot_expense_pie():
    # Retrieve expense data from the database
    cursor.execute("SELECT name, amount FROM expenses")
    expenses = cursor.fetchall()

    # Separate expense names and amounts
    names = [expense[0] for expense in expenses]
    amounts = [expense[1] for expense in expenses]

    # Create a color palette for the pie chart
    colors = plt.cm.Set3(np.linspace(0, 1, len(names)))

    # Plot the pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(amounts, labels=names, colors=colors, autopct='%1.1f%%')
    plt.title("Expense Breakdown")
    plt.axis('equal')
    plt.show()

# Create the balance tab
tab_balance = ttk.Frame(window)
tab_balance.pack(fill='both', expand=True)

label_balance = tk.Label(tab_balance, text="Current Balance:", font=("Arial", 18))
label_balance.pack(pady=10)

button_update_balance = tk.Button(tab_balance, text="Update Balance", command=update_balance)
button_update_balance.pack(pady=5)

# Create the expenses tab
tab_expenses = ttk.Frame(window)
tab_expenses.pack(fill='both', expand=True)

frame_expense_input = tk.Frame(tab_expenses)
frame_expense_input.pack(pady=20)

label_expense = tk.Label(frame_expense_input, text="Expense:", font=("Arial", 18))
label_expense.grid(row=0, column=0, padx=5)

combo_expense = ttk.Combobox(frame_expense_input, values=expense_names)
combo_expense.grid(row=0, column=1, padx=5)

button_add_expense = tk.Button(frame_expense_input, text="Add Expense", command=add_expense)
button_add_expense.grid(row=0, column=2, padx=5)

frame_expense_history = tk.Frame(tab_expenses)
frame_expense_history.pack(pady=20)

label_expense_history = tk.Label(frame_expense_history, text="Expense History:", font=("Arial", 18))
label_expense_history.pack()

text_expense_history = tk.Text(frame_expense_history, width=40, height=10, state=tk.DISABLED)
text_expense_history.pack()

button_plot_expenses = tk.Button(tab_expenses, text="Plot Expense Breakdown", command=plot_expense_breakdown)
button_plot_expenses.pack(pady=10)

# Create the plot expenses pie button
button_plot_pie = tk.Button(tab_expenses, text="Plot Expenses Pie", command=plot_expense_pie)
button_plot_pie.pack(pady=10)

button_reset = tk.Button(tab_expenses, text="Reset App", command=reset_app)
button_reset.pack(pady=10)

# Run the application
update_balance()
update_expense_history()
window.mainloop()

# Close the database connection
connection.close()

