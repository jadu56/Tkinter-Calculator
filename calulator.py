import tkinter as tk
from tkinter import font


class Calculator:
    def __init__(self, root):
        self.previous_label = None
        self.display = None
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("300x400")
        self.root.resizable(False, False)

        # Initialize variables
        self.current_input = "0"
        self.previous_input = ""
        self.operation = None
        self.reset_next_input = False

        # Create custom font
        self.display_font = font.Font(size=24)
        self.button_font = font.Font(size=12, weight="bold")

        self.create_widgets()

    def create_widgets(self):
        # Display frame
        display_frame = tk.Frame(self.root, height=100)
        display_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Previous calculation display (smaller)
        self.previous_label = tk.Label(
            display_frame,
            text=self.previous_input,
            anchor="e",
            font=("Arial", 10),
            fg="gray"
        )
        self.previous_label.pack(expand=True, fill="both")

        # Current input display
        self.display = tk.Label(
            display_frame,
            text=self.current_input,
            anchor="e",
            font=self.display_font,
            bg="white",
            relief="sunken",
            bd=2
        )
        self.display.pack(expand=True, fill="both")

        # Button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Button layout
        buttons = [
            ['C', '⌫', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['00', '0', '.', '=']
        ]

        # Create buttons
        for i, row in enumerate(buttons):
            button_frame.rowconfigure(i, weight=1)
            for j, btn_text in enumerate(row):
                button_frame.columnconfigure(j, weight=1)

                btn = tk.Button(
                    button_frame,
                    text=btn_text,
                    font=self.button_font,
                    command=lambda text=btn_text: self.on_button_click(text)
                )

                # Color coding
                if btn_text in ['C', '⌫']:
                    btn.config(bg="#ff6666", fg="white")
                elif btn_text in ['/', '*', '-', '+', '=']:
                    btn.config(bg="#4682B4", fg="white")
                elif btn_text == '%':
                    btn.config(bg="#90EE90")
                else:
                    btn.config(bg="#f0f0f0")

                btn.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)

    def on_button_click(self, text):
        if text in '0123456789':
            self.input_digit(text)
        elif text == '.':
            self.input_decimal()
        elif text == '00':
            self.input_double_zero()
        elif text in ['+', '-', '*', '/']:
            self.set_operation(text)
        elif text == '=':
            self.calculate()
        elif text == 'C':
            self.clear()
        elif text == '⌫':
            self.backspace()
        elif text == '%':
            self.percentage()

        self.update_display()

    def input_digit(self, digit):
        if self.current_input == "0" or self.reset_next_input:
            self.current_input = digit
            self.reset_next_input = False
        else:
            self.current_input += digit

    def input_decimal(self):
        if self.reset_next_input:
            self.current_input = "0."
            self.reset_next_input = False
        elif "." not in self.current_input:
            self.current_input += "."

    def input_double_zero(self):
        if self.current_input != "0":
            self.current_input += "00"

    def set_operation(self, op):
        if self.operation and not self.reset_next_input:
            self.calculate()

        self.previous_input = self.current_input
        self.operation = op
        self.reset_next_input = True

    def calculate(self):
        global result
        if not self.operation or self.reset_next_input:
            return

        try:
            prev = float(self.previous_input)
            curr = float(self.current_input)

            if self.operation == '+':
                result = prev + curr
            elif self.operation == '-':
                result = prev - curr
            elif self.operation == '*':
                result = prev * curr
            elif self.operation == '/':
                if curr == 0:
                    self.current_input = "Error"
                    self.reset_next_input = True
                    return
                result = prev / curr

            # Format result to avoid unnecessary decimal places
            if result.is_integer():
                self.current_input = str(int(result))
            else:
                self.current_input = str(round(result, 10)).rstrip('0').rstrip('.')

        except:
            self.current_input = "Error"

        self.operation = None
        self.reset_next_input = True

    def clear(self):
        self.current_input = "0"
        self.previous_input = ""
        self.operation = None
        self.reset_next_input = False

    def backspace(self):
        if self.current_input == "Error":
            self.clear()
        elif len(self.current_input) > 1:
            self.current_input = self.current_input[:-1]
        else:
            self.current_input = "0"

    def percentage(self):
        try:
            value = float(self.current_input) / 100
            if value.is_integer():
                self.current_input = str(int(value))
            else:
                self.current_input = str(value)
        except:
            self.current_input = "Error"
            self.reset_next_input = True

    def update_display(self):
        # Update main display
        self.display.config(text=self.current_input)

        # Update previous calculation display
        if self.operation:
            self.previous_label.config(text=f"{self.previous_input} {self.operation}")
        else:
            self.previous_label.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()