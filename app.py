import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  # Importing the DateEntry widget from tkcalendar
import sqlite3

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("500x400")  # Increased size for better layout
        
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#2C3E50')  # Dark blue background
        self.style.configure('TButton', background='#1ABC9C', foreground='#FFFFFF', font=('Arial', 14, 'bold'))  # Teal button with white text
        self.style.configure('TLabel', background='#2C3E50', foreground='#ECF0F1', font=('Arial', 16, 'bold'))  # Light gray text
        
        self.create_database()  # Ensure database is created first
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")
        
        self.add_expense_frame = tk.Frame(self.notebook, bg='#2C3E50')
        self.summary_frame = tk.Frame(self.notebook, bg='#2C3E50')
        self.filter_frame = tk.Frame(self.notebook, bg='#2C3E50')
        
        self.notebook.add(self.add_expense_frame, text="Add Expense")
        self.notebook.add(self.summary_frame, text="Summary")
        self.notebook.add(self.filter_frame, text="Filter Expenses")
        
        self.create_add_expense_page()
        self.create_summary_page()
        self.create_filter_page()
    
    def create_database(self):
        self.conn = sqlite3.connect('expenses.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS expenses
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             date TEXT,
                             category TEXT,
                             amount REAL)''')
        self.conn.commit()
        
    def create_add_expense_page(self):
        tk.Label(self.add_expense_frame, text="Date:", font=('Arial', 16, 'bold'), bg='#2C3E50', fg='#ECF0F1').grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        self.entry_date = DateEntry(self.add_expense_frame, font=('Arial', 14), background='darkblue', foreground='white', borderwidth=2)
        self.entry_date.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        tk.Label(self.add_expense_frame, text="Category:", font=('Arial', 16, 'bold'), bg='#2C3E50', fg='#ECF0F1').grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        self.entry_category = ttk.Combobox(self.add_expense_frame, font=('Arial', 14), state="readonly")
        self.entry_category['values'] = ("Groceries", "Utilities", "Transportation", "Entertainment", "Dining")
        self.entry_category.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        tk.Label(self.add_expense_frame, text="Amount (₹):", font=('Arial', 16, 'bold'), bg='#2C3E50', fg='#ECF0F1').grid(row=2, column=0, padx=5, pady=5, sticky='ew')
        self.entry_amount = tk.Entry(self.add_expense_frame, font=('Arial', 14))
        self.entry_amount.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        
        tk.Button(self.add_expense_frame, text="Add Expense", command=self.add_expense, bg='#1ABC9C', fg='#FFFFFF', font=('Arial', 14, 'bold')).grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        tk.Button(self.add_expense_frame, text="Clear Fields", command=self.clear_fields, bg='#E74C3C', fg='#FFFFFF', font=('Arial', 14, 'bold')).grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
    
    def create_summary_page(self):
        self.label_total_expenses = tk.Label(self.summary_frame, text="Total Expenses: ₹0.00", font=("Arial", 18, "bold"), bg='#2C3E50', fg='#ECF0F1')
        self.label_total_expenses.pack(padx=10, pady=10)
        self.update_total_expenses()
        
        # Button to clear the summary manually
        tk.Button(self.summary_frame, text="Clear Summary", command=self.clear_summary, bg='#E74C3C', fg='#FFFFFF', font=('Arial', 14, 'bold')).pack(pady=10)
    
    def create_filter_page(self):
        tk.Label(self.filter_frame, text="Category:", font=('Arial', 16, 'bold'), bg='#2C3E50', fg='#ECF0F1').grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        self.filter_category = ttk.Combobox(self.filter_frame, font=('Arial', 14), state="readonly")
        self.filter_category['values'] = ("All", "Groceries", "Utilities", "Transportation", "Entertainment", "Dining")
        self.filter_category.current(0)
        self.filter_category.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        tk.Button(self.filter_frame, text="Apply Filter", command=self.apply_filter, bg='#1ABC9C', fg='#FFFFFF', font=('Arial', 14, 'bold')).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
    
    def add_expense(self):
        date = self.entry_date.get()
        category = self.entry_category.get()
        amount = self.entry_amount.get()
        
        if not (date and category and amount):
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        try:
            amount = float(amount)
            self.c.execute("INSERT INTO expenses (date, category, amount) VALUES (?, ?, ?)", (date, category, amount))
            self.conn.commit()
            messagebox.showinfo("Success", "Expense added successfully.")
            self.clear_fields()  # Clear fields after adding expense
            self.update_total_expenses()  # Update summary
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
    
    def update_total_expenses(self):
        total_expenses = self.c.execute("SELECT SUM(amount) FROM expenses").fetchone()[0]
        if total_expenses is not None:
            total_expenses = f"Total Expenses: ₹{total_expenses:.2f}"
        else:
            total_expenses = "Total Expenses: ₹0.00"
        self.label_total_expenses.config(text=total_expenses)
    
    def clear_summary(self):
        self.label_total_expenses.config(text="Total Expenses: ₹0.00")

    def apply_filter(self):
        category = self.filter_category.get()
        if category == "All":
            filtered_expenses = self.c.execute("SELECT * FROM expenses").fetchall()
        else:
            filtered_expenses = self.c.execute("SELECT * FROM expenses WHERE category=?", (category,)).fetchall()
    
        # Display filtered expenses
        self.display_filtered_expenses(filtered_expenses)

    def display_filtered_expenses(self, expenses):
        self.filtered_window = tk.Toplevel(self.root)
        self.filtered_window.title("Filtered Expenses")
        self.filtered_window.config(bg='#2C3E50')

        tk.Label(self.filtered_window, text="Date", font=('Arial', 16, 'bold'), bg='#2C3E50', fg='#ECF0F1').grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        tk.Label(self.filtered_window, text="Category", font=('Arial', 16, 'bold'), bg='#2C3E50', fg='#ECF0F1').grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        tk.Label(self.filtered_window, text="Amount (₹)", font=('Arial', 16, 'bold'), bg='#2C3E50', fg='#ECF0F1').grid(row=0, column=2, padx=5, pady=5, sticky='ew')
        
        for i, expense in enumerate(expenses, start=1):
            tk.Label(self.filtered_window, text=expense[1], font=('Arial', 14), bg='#2C3E50', fg='#ECF0F1').grid(row=i, column=0, padx=5, pady=5, sticky='ew')
            tk.Label(self.filtered_window, text=expense[2], font=('Arial', 14), bg='#2C3E50', fg='#ECF0F1').grid(row=i, column=1, padx=5, pady=5, sticky='ew')
            tk.Label(self.filtered_window, text=f"₹{expense[3]:.2f}", font=('Arial', 14), bg='#2C3E50', fg='#ECF0F1').grid(row=i, column=2, padx=5, pady=5, sticky='ew')

    def clear_fields(self):
        self.entry_date.delete(0, tk.END)
        self.entry_category.set('')
        self.entry_amount.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
