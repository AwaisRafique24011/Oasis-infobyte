import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# Database setup
def create_database():
    conn = sqlite3.connect('C:/Users/Faiza/Desktop/done python project/bmi_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bmi_data (
            id INTEGER PRIMARY KEY,
            user_name TEXT,
            weight REAL,
            height REAL,
            bmi REAL,
            category TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_database()

# Main Application
class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")

        # UI Elements
        tk.Label(root, text="Name:").grid(row=0, column=0, pady=5)
        tk.Label(root, text="Weight (kg):").grid(row=1, column=0, pady=5)
        tk.Label(root, text="Height (m):").grid(row=2, column=0, pady=5)

        self.name_entry = tk.Entry(root)
        self.weight_entry = tk.Entry(root)
        self.height_entry = tk.Entry(root)

        self.name_entry.grid(row=0, column=1, pady=5)
        self.weight_entry.grid(row=1, column=1, pady=5)
        self.height_entry.grid(row=2, column=1, pady=5)

        tk.Button(root, text="Calculate BMI", command=self.calculate_bmi).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(root, text="View History", command=self.view_history).grid(row=4, column=0, columnspan=2, pady=5)
        tk.Button(root, text="Analyze Trends", command=self.analyze_trends).grid(row=5, column=0, columnspan=2, pady=5)

        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=6, column=0, columnspan=2, pady=10)

    def calculate_bmi(self):
        name = self.name_entry.get()
        weight = self.weight_entry.get()
        height = self.height_entry.get()

        if not name or not weight or not height:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            weight = float(weight)
            height = float(height)
            if weight <= 0 or height <= 0:
                raise ValueError("Invalid value for weight or height.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numerical values for weight and height.")
            return

        bmi = weight / (height ** 2)
        category = self.categorize_bmi(bmi)

        self.result_label.config(text=f"BMI: {bmi:.2f} ({category})")

        self.save_bmi_data(name, weight, height, bmi, category)

    def categorize_bmi(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"

    def save_bmi_data(self, name, weight, height, bmi, category):
        conn = sqlite3.connect('bmi_data.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO bmi_data (user_name, weight, height, bmi, category, date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, weight, height, bmi, category, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()

    def view_history(self):
        conn = sqlite3.connect('bmi_data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM bmi_data WHERE user_name = ?", (self.name_entry.get(),))
        records = c.fetchall()
        conn.close()

        if not records:
            messagebox.showinfo("History", "No records found for this user.")
            return

        history_window = tk.Toplevel(self.root)
        history_window.title("BMI History")

        tk.Label(history_window, text="Date").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(history_window, text="Weight (kg)").grid(row=0, column=1, padx=10, pady=10)
        tk.Label(history_window, text="Height (m)").grid(row=0, column=2, padx=10, pady=10)
        tk.Label(history_window, text="BMI").grid(row=0, column=3, padx=10, pady=10)
        tk.Label(history_window, text="Category").grid(row=0, column=4, padx=10, pady=10)

        for i, record in enumerate(records, start=1):
            tk.Label(history_window, text=record[6]).grid(row=i, column=0, padx=10, pady=5)
            tk.Label(history_window, text=record[2]).grid(row=i, column=1, padx=10, pady=5)
            tk.Label(history_window, text=record[3]).grid(row=i, column=2, padx=10, pady=5)
            tk.Label(history_window, text=f"{record[4]:.2f}").grid(row=i, column=3, padx=10, pady=5)
            tk.Label(history_window, text=record[5]).grid(row=i, column=4, padx=10, pady=5)

    def analyze_trends(self):
        conn = sqlite3.connect('bmi_data.db')
        c = conn.cursor()
        c.execute("SELECT date, bmi FROM bmi_data WHERE user_name = ? ORDER BY date", (self.name_entry.get(),))
        records = c.fetchall()
        conn.close()

        if not records:
            messagebox.showinfo("Trends", "No data available to analyze.")
            return

        dates = [record[0] for record in records]
        bmis = [record[1] for record in records]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, bmis, marker='o', linestyle='-', color='b')
        plt.xlabel("Date")
        plt.ylabel("BMI")
        plt.title("BMI Trend Analysis")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()
