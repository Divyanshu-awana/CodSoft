import tkinter as tk
from tkinter import ttk, messagebox

def add_num(num1, num2):
    return num1 + num2

def sub_num(num1, num2):
    return num1 - num2

def mul_num(num1, num2):
    return num1 * num2

def div_num(num1, num2):
    if num2 == 0:
        raise ZeroDivisionError("Division by zero is not allowed.")
    return num1 / num2

class CalculatorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Modern Calculator")
        master.geometry("400x300")
        master.configure(bg="#222831")  # modern dark theme

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background="#222831", foreground="#DFD0B8", font=("Poppins", 14))
        style.configure('TButton', font=("Poppins", 13), padding=10)
        style.configure('TEntry', font=("Poppins", 14), fieldbackground="#948979", foreground="#393E46")

        # Entry fields for numbers
        self.num1_entry = ttk.Entry(master, width=16)
        self.num2_entry = ttk.Entry(master, width=16)
        self.num1_entry.grid(row=0, column=1, padx=14, pady=18, sticky='ew')
        self.num2_entry.grid(row=1, column=1, padx=14, pady=18, sticky='ew')

        ttk.Label(master, text="First Number:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        ttk.Label(master, text="Second Number:").grid(row=1, column=0, padx=10, pady=10, sticky='w')

        # Operation buttons
        btn_frame = ttk.Frame(master)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        btn_frame.configure(style="TFrame")

        btn_texts = [
            ("+", self.add),
            ("-", self.subtract),
            ("×", self.multiply),
            ("÷", self.divide)
        ]
        for idx, (text, cmd) in enumerate(btn_texts):
            btn = ttk.Button(btn_frame, text=text, width=5, command=cmd)
            btn.grid(row=0, column=idx, padx=12)

        # Result display
        self.result_var = tk.StringVar()
        ttk.Label(master, text="Result:").grid(row=3, column=0, padx=10, sticky='w')
        res_label = ttk.Label(master, textvariable=self.result_var, font=("Poppins", 16, "bold"), foreground="#8be9fd")
        res_label.grid(row=3, column=1, padx=10, sticky='ew')

    def _get_inputs(self):
        try:
            num1 = float(self.num1_entry.get())
            num2 = float(self.num2_entry.get())
            return num1, num2
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.")
            return None, None

    def add(self):
        num1, num2 = self._get_inputs()
        if num1 is not None:
            self.result_var.set(str(add_num(num1, num2)))

    def subtract(self):
        num1, num2 = self._get_inputs()
        if num1 is not None:
            self.result_var.set(str(sub_num(num1, num2)))

    def multiply(self):
        num1, num2 = self._get_inputs()
        if num1 is not None:
            self.result_var.set(str(mul_num(num1, num2)))

    def divide(self):
        num1, num2 = self._get_inputs()
        if num1 is not None:
            try:
                result = div_num(num1, num2)
                self.result_var.set(str(result))
            except ZeroDivisionError:
                messagebox.showerror("Math Error", "You can't divide by zero.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()
