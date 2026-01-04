import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import math
import urllib.request
import json

class MultiCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi Calculator App")
        self.geometry("500x650")

        # Define themes
        self.themes = {
            "Dark": {
                "bg": "#2c3e50",
                "fg": "white",
                "button_bg": "#2980b9",
                "button_fg": "white",
                "entry_bg": "#ecf0f1",
                "entry_fg": "black",
                "highlight": "#1abc9c"
            },
            "Light": {
                "bg": "#f5f6fa",
                "fg": "black",
                "button_bg": "#3498db",
                "button_fg": "white",
                "entry_bg": "white",
                "entry_fg": "black",
                "highlight": "#2980b9"
            }
        }

        self.current_theme = "Dark"
        self.configure(bg=self.themes[self.current_theme]["bg"])

        # Dropdown variables
        self.calculator_var = tk.StringVar(value="Normal Calculator")
        self.theme_var = tk.StringVar(value=self.current_theme)

        options = ["Normal Calculator", "Scientific Calculator", "BMI Calculator", "Age Calculator", "Currency Converter"]

        # Top frame for dropdowns
        top_frame = tk.Frame(self, bg=self.themes[self.current_theme]["bg"])
        top_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        top_frame.grid_columnconfigure(0, weight=1)
        top_frame.grid_columnconfigure(1, weight=0)

        # Calculator dropdown
        calc_dropdown = ttk.OptionMenu(top_frame, self.calculator_var, options[0], *options, command=self.show_calculator)
        calc_dropdown.grid(row=0, column=0, sticky='e', padx=(0, 10))

        # Theme dropdown
        theme_dropdown = ttk.OptionMenu(top_frame, self.theme_var, self.current_theme, *self.themes.keys(), command=self.change_theme)
        theme_dropdown.grid(row=0, column=1, sticky='e')

        # Container for calculators
        self.container = tk.Frame(self, bg=self.themes[self.current_theme]["bg"])
        self.container.grid(row=1, column=0, sticky='nsew', padx=20, pady=15)

        # Grid config for resizing
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (NormalCalc, ScientificCalc, BMICalc, AgeCalc, CurrencyConverter):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_calculator(options[0])
        self.change_theme(self.current_theme)

    def show_calculator(self, name):
        mapping = {
            "Normal Calculator": "NormalCalc",
            "Scientific Calculator": "ScientificCalc",
            "BMI Calculator": "BMICalc",
            "Age Calculator": "AgeCalc",
            "Currency Converter": "CurrencyConverter"
        }
        frame_name = mapping.get(name)
        if frame_name and frame_name in self.frames:
            self.frames[frame_name].tkraise()
        else:
            messagebox.showerror("Error", f"Calculator frame for '{name}' not found!")

    def change_theme(self, theme_name):
        self.current_theme = theme_name
        colors = self.themes[theme_name]
        self.configure(bg=colors["bg"])
        self.container.configure(bg=colors["bg"])
        for frame in self.frames.values():
            frame.update_theme(colors)

################ Normal Calculator #################
class NormalCalc(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.expression = ""
        self.input_text = tk.StringVar()

        self.configure(bg=controller.themes[controller.current_theme]["bg"])
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.input_field = tk.Entry(self, font=('Segoe UI', 24, 'bold'), textvariable=self.input_text, bd=3,
                                    relief=tk.FLAT, justify='right')
        self.input_field.grid(row=0, column=0, sticky='ew', padx=10, pady=(20,10), ipady=12)

        self.btns_frame = tk.Frame(self)
        self.btns_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        buttons = [
            ['7', '8', '9', '+'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '*'],
            ['0', '.', 'C', '/'],
            ['=']
        ]

        self.buttons = []
        for r, row in enumerate(buttons):
            self.btns_frame.grid_rowconfigure(r, weight=1)
            for c, char in enumerate(row):
                self.btns_frame.grid_columnconfigure(c, weight=1)
                btn = tk.Button(self.btns_frame, text=char, font=('Segoe UI', 18), relief=tk.RAISED, bd=0,
                                command=lambda ch=char: self.on_button_click(ch))
                btn.grid(row=r, column=c, sticky='nsew', padx=3, pady=3)
                self.buttons.append(btn)

        self.update_theme(controller.themes[controller.current_theme])

    def on_button_click(self, char):
        if char == 'C':
            self.expression = ""
        elif char == '=':
            try:
                result = str(eval(self.expression))
                self.expression = result
            except:
                self.expression = ""
                result = "Error"
            self.input_text.set(result)
            return
        else:
            self.expression += char
        self.input_text.set(self.expression)

    def update_theme(self, colors):
        self.configure(bg=colors["bg"])
        self.input_field.config(bg=colors["entry_bg"], fg=colors["entry_fg"], insertbackground=colors["fg"])
        self.btns_frame.config(bg=colors["bg"])
        for btn in self.buttons:
            btn.config(bg=colors["button_bg"], fg=colors["button_fg"],
                       activebackground=colors["highlight"], activeforeground=colors["button_fg"])

################ Scientific Calculator #################
class ScientificCalc(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.expression = ""
        self.input_text = tk.StringVar()

        self.configure(bg=controller.themes[controller.current_theme]["bg"])
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.input_field = tk.Entry(self, font=('Segoe UI', 24, 'bold'), textvariable=self.input_text, bd=3,
                                    relief=tk.FLAT, justify='right')
        self.input_field.grid(row=0, column=0, sticky='ew', padx=10, pady=(20,10), ipady=12)

        self.btns_frame = tk.Frame(self)
        self.btns_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        buttons = [
            ['7', '8', '9', '/', 'sqrt'],
            ['4', '5', '6', '*', 'log'],
            ['1', '2', '3', '-', 'sin'],
            ['0', '.', '=', '+', 'cos'],
            ['C', '(', ')', '^', 'tan']
        ]

        self.buttons = []
        for r, row in enumerate(buttons):
            self.btns_frame.grid_rowconfigure(r, weight=1)
            for c, char in enumerate(row):
                self.btns_frame.grid_columnconfigure(c, weight=1)
                btn = tk.Button(self.btns_frame, text=char, font=('Segoe UI', 16), relief=tk.FLAT, bd=0,
                                command=lambda ch=char: self.on_button_click(ch))
                btn.grid(row=r, column=c, sticky='nsew', padx=5, pady=3)
                self.buttons.append(btn)

        self.update_theme(controller.themes[controller.current_theme])

    def on_button_click(self, char):
        if char == 'C':
            self.expression = ""
            self.input_text.set("")
        elif char == '=':
            try:
                expr = self.expression.replace('^', '**')
                expr = expr.replace('sqrt', 'math.sqrt')
                expr = expr.replace('log', 'math.log10')
                expr = expr.replace('sin', 'math.sin(math.radians')
                expr = expr.replace('cos', 'math.cos(math.radians')
                expr = expr.replace('tan', 'math.tan(math.radians')
                trig_funcs = ['math.sin(math.radians', 'math.cos(math.radians', 'math.tan(math.radians']
                for func in trig_funcs:
                    expr += ')' * expr.count(func)
                import math
                result = eval(expr)
                if isinstance(result, float):
                    result = round(result, 8)
                self.expression = str(result)
                self.input_text.set(result)
            except Exception:

                self.input_text.set("Error")
                self.expression = ""
        else:
            self.expression += char
            self.input_text.set(self.expression)

    def update_theme(self, colors):
        self.configure(bg=colors["bg"])
        self.input_field.config(bg=colors["entry_bg"], fg=colors["entry_fg"], insertbackground=colors["fg"])
        self.btns_frame.config(bg=colors["bg"])
        for btn in self.buttons:
            btn.config(bg=colors["button_bg"], fg=colors["button_fg"],
                       activebackground=colors["highlight"], activeforeground=colors["button_fg"])

############### BMI Calculator #################
class BMICalc(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=controller.themes[controller.current_theme]["bg"])

        self.grid_rowconfigure(6, weight=1)
        self.grid_columnconfigure(0, weight=1)

        tk.Label(self, text="BMI Calculator", font=("Segoe UI", 24, 'bold'), fg=controller.themes[controller.current_theme]["fg"],
                 bg=controller.themes[controller.current_theme]["bg"]).grid(row=0, column=0, pady=20, sticky='n')

        self.weight_var = tk.StringVar()
        self.height_var = tk.StringVar()
        self.result_var = tk.StringVar()

        tk.Label(self, text="Weight (kg):", font=("Segoe UI", 16), fg=controller.themes[controller.current_theme]["fg"],
                 bg=controller.themes[controller.current_theme]["bg"]).grid(row=1, column=0, sticky='w', padx=30)
        tk.Entry(self, textvariable=self.weight_var, font=("Segoe UI", 16), bd=3,
                 relief=tk.FLAT).grid(row=2, column=0, sticky='ew', padx=30, pady=5)

        tk.Label(self, text="Height (cm):", font=("Segoe UI", 16), fg=controller.themes[controller.current_theme]["fg"],
                 bg=controller.themes[controller.current_theme]["bg"]).grid(row=3, column=0, sticky='w', padx=30)
        tk.Entry(self, textvariable=self.height_var, font=("Segoe UI", 16), bd=3, relief=tk.FLAT).grid(row=4,
                 column=0, sticky='ew', padx=30, pady=5)

        tk.Button(self, text="Calculate BMI", font=("Segoe UI", 16, 'bold'), bg=controller.themes[controller.current_theme]["button_bg"],
                  fg=controller.themes[controller.current_theme]["button_fg"], relief=tk.FLAT,
                  command=self.calculate_bmi).grid(row=5, column=0, pady=20, ipadx=10, ipady=5)

        tk.Label(self, textvariable=self.result_var, font=("Segoe UI", 18, 'bold'), fg="#1abc9c",
                 bg=controller.themes[controller.current_theme]["bg"]).grid(row=6, column=0, pady=15)

    def calculate_bmi(self):
        try:
            weight = float(self.weight_var.get())
            height_cm = float(self.height_var.get())
            height_m = height_cm / 100
            bmi = weight / (height_m ** 2)
            bmi = round(bmi, 2)
            if bmi < 18.5:
                category = "Underweight"
            elif bmi < 25:
                category = "Normal weight"
            elif bmi < 30:
                category = "Overweight"
            else:
                category = "Obese"
            self.result_var.set(f"BMI: {bmi} ({category})")
        except:
            self.result_var.set("Invalid Input")

############### Age Calculator #################
class AgeCalc(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=controller.themes[controller.current_theme]["bg"])

        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)

        tk.Label(self, text="Age Calculator", font=("Segoe UI", 24, 'bold'), fg=controller.themes[controller.current_theme]["fg"],
                 bg=controller.themes[controller.current_theme]["bg"]).grid(row=0, column=0, pady=20, sticky='n')

        self.dob_var = tk.StringVar()
        self.age_var = tk.StringVar()

        tk.Label(self, text="Enter Date of Birth (YYYY-MM-DD):", font=("Segoe UI", 16), fg=controller.themes[controller.current_theme]["fg"],
                 bg=controller.themes[controller.current_theme]["bg"]).grid(row=1, column=0, sticky='w', padx=30)
        tk.Entry(self, textvariable=self.dob_var, font=("Segoe UI", 16), bd=3, relief=tk.FLAT).grid(row=2, column=0, sticky='ew', padx=30, pady=5)

        tk.Button(self, text="Calculate Age", font=("Segoe UI", 16, 'bold'), bg=controller.themes[controller.current_theme]["button_bg"],
                  fg=controller.themes[controller.current_theme]["button_fg"], relief=tk.FLAT,
                  command=self.calculate_age).grid(row=3, column=0, pady=20, ipadx=10, ipady=5)

        tk.Label(self, textvariable=self.age_var, font=("Segoe UI", 18, 'bold'), fg="#1abc9c",
                 bg=controller.themes[controller.current_theme]["bg"]).grid(row=4, column=0, pady=15)

    def calculate_age(self):
        try:
            dob_str = self.dob_var.get()
            dob = datetime.strptime(dob_str, "%Y-%m-%d")
            today = datetime.today()
            age_years = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            self.age_var.set(f"Your age is: {age_years} years")
        except:
            self.age_var.set("Invalid Date Format")

############### Currency Converter #################
class CurrencyConverter(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=controller.themes[controller.current_theme]["bg"])

        self.grid_rowconfigure(8, weight=1)
        self.grid_columnconfigure(0, weight=1)

        tk.Label(self, text="Currency Converter", font=("Segoe UI", 24, 'bold'),fg=controller.themes[controller.current_theme]["fg"],
                 bg=controller.themes[controller.current_theme]["bg"]).grid(row=0, column=0, pady=20, sticky='n')

        self.amount_var = tk.StringVar()
        self.from_currency_var = tk.StringVar(value="USD")
        self.to_currency_var = tk.StringVar(value="INR")
        self.converted_var = tk.StringVar()

        tk.Label(self, text="Amount", font=("Segoe UI", 16), fg=controller.themes[controller.current_theme]["fg"],
                 bg=controller.themes[controller.current_theme]["bg"]).grid(row=1, column=0, sticky='w', padx=30)
        tk.Entry(self, textvariable=self.amount_var, font=("Segoe UI", 16), bd=3, relief=tk.FLAT).grid(row=2, column=0, sticky='ew', padx=30, pady=5)

        currencies = ['USD', 'INR', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'CNY']

        tk.Label(self, text="From Currency", font=("Segoe UI", 16), fg=controller.themes[controller.current_theme]["fg"],
                 bg=controller.themes[controller.current_theme]["bg"]).grid(row=3, column=0, sticky='w', padx=30)
        from_menu = ttk.Combobox(self, values=currencies, textvariable=self.from_currency_var,
                                 state='readonly', font=("Segoe UI", 16))
        from_menu.grid(row=4, column=0, sticky='ew', padx=30, pady=5)

        tk.Label(self, text="To Currency", font=("Segoe UI", 16), fg=controller.themes[controller.current_theme]["fg"],
                 bg=controller.themes[controller.current_theme]["bg"]).grid(row=5, column=0, sticky='w', padx=30)
        to_menu = ttk.Combobox(self, values=currencies, textvariable=self.to_currency_var, state='readonly', font=("Segoe UI", 16))
        to_menu.grid(row=6, column=0, sticky='ew', padx=30, pady=5)

        tk.Button(self, text="Convert", font=("Segoe UI", 16, 'bold'),
                  bg=controller.themes[controller.current_theme]["button_bg"],
                  fg=controller.themes[controller.current_theme]["button_fg"], relief=tk.FLAT,
                  command=self.convert_currency).grid(row=7, column=0, pady=20, ipadx=10, ipady=5)

        tk.Label(self, textvariable=self.converted_var, font=("Segoe UI", 18, 'bold'), fg="#1abc9c",
                 bg=controller.themes[controller.current_theme]["bg"]).grid(row=8, column=0, pady=10)

    def convert_currency(self):
        try:
            amount = float(self.amount_var.get())
            from_cur = self.from_currency_var.get()
            to_cur = self.to_currency_var.get()

            rates = self.get_rates(from_cur)

            if to_cur not in rates:
                self.converted_var.set(f"Conversion rate for {to_cur} not found.")
                return

            converted_amount = amount * rates[to_cur]
            self.converted_var.set(f"{amount} {from_cur} = {round(converted_amount, 4)} {to_cur}")

        except ValueError:
            self.converted_var.set("Invalid amount")
        except Exception:
            self.converted_var.set("Conversion Failed")

    def get_rates(self, base):
        url = f"https://api.exchangerate-api.com/v4/latest/{base}"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
        return data.get("rates", {})

if __name__ == "__main__":
    MultiCalculatorApp().mainloop()

