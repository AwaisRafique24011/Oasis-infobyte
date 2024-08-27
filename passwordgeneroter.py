import tkinter as tk
from tkinter import messagebox
from tkinter import StringVar, IntVar
import random
import string
import pyperclip

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Generator")

        # Password options
        self.length = IntVar(value=12)
        self.include_uppercase = IntVar(value=1)
        self.include_numbers = IntVar(value=1)
        self.include_symbols = IntVar(value=1)
        self.password = StringVar()

        # GUI Layout
        tk.Label(root, text="Password Length:").grid(row=0, column=0, pady=5, padx=5)
        tk.Spinbox(root, from_=8, to_=32, textvariable=self.length, width=5).grid(row=0, column=1, pady=5, padx=5)

        tk.Checkbutton(root, text="Include Uppercase", variable=self.include_uppercase).grid(row=1, column=0, columnspan=2, sticky='w')
        tk.Checkbutton(root, text="Include Numbers", variable=self.include_numbers).grid(row=2, column=0, columnspan=2, sticky='w')
        tk.Checkbutton(root, text="Include Symbols", variable=self.include_symbols).grid(row=3, column=0, columnspan=2, sticky='w')

        tk.Button(root, text="Generate Password", command=self.generate_password).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Entry(root, textvariable=self.password, width=40).grid(row=5, column=0, columnspan=2, pady=5, padx=5)
        tk.Button(root, text="Copy to Clipboard", command=self.copy_to_clipboard).grid(row=6, column=0, columnspan=2, pady=5)

    def generate_password(self):
        length = self.length.get()
        include_uppercase = self.include_uppercase.get()
        include_numbers = self.include_numbers.get()
        include_symbols = self.include_symbols.get()

        # Character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase if include_uppercase else ''
        numbers = string.digits if include_numbers else ''
        symbols = string.punctuation if include_symbols else ''

        # Combine selected character sets
        all_characters = lowercase + uppercase + numbers + symbols

        if not all_characters:
            messagebox.showerror("Error", "No character sets selected! Please select at least one option.")
            return

        # Generate the password
        password = ''.join(random.choice(all_characters) for _ in range(length))
        self.password.set(password)

    def copy_to_clipboard(self):
        pyperclip.copy(self.password.get())
        messagebox.showinfo("Copied", "Password copied to clipboard!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
