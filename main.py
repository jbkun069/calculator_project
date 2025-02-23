import tkinter as tk
from tkinter import Menu
import math
import re

class Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculator")
        self.master.geometry("400x500")
        self.master.configure(bg='#1a1a1a')

        # Theme setup
        self.theme = "dark"
        self.light_theme = {'bg': 'white', 'fg': 'black', 'button_bg': '#f0f0f0', 'button_fg': '#ff8c00'}
        self.dark_theme = {'bg': '#1a1a1a', 'fg': 'white', 'button_bg': '#333333', 'button_fg': '#ff8c00'}
        self.current_theme = self.dark_theme

        # Display setup
        self.display_var = tk.StringVar(value="0")
        self.display = tk.Entry(self.master, textvariable=self.display_var, font=('Arial', 20, 'bold'), justify='right',
                               bg='#000000', fg='#ffffff', insertbackground='#ffffff', relief='flat')
        self.display.grid(row=0, column=0, columnspan=4, sticky='nsew', padx=10, pady=10)
        self.display.bind('<Key>', lambda e: 'break')  # Prevent direct keyboard input
        
        # Track cursor position
        self.display.icursor(0)

        # Button layout
        self.buttons = []
        buttons_layout = [
            ['AC', 'DEL', '%', '+'],
            ['7', '8', '9', '-'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '/'],
            ['0', '.', '=', 'sqrt'],
            ['fact', 'pi', '(', ')'],
            ['1/x', '^', '+/-', '']
        ]

        for row in range(7):
            for col in range(4):
                label = buttons_layout[row][col]
                if label:
                    button = tk.Button(self.master, text=label, font=('Arial', 14, 'bold'), width=7, height=2,
                                      bg=self.current_theme['button_bg'], fg=self.current_theme['button_fg'],
                                      relief='flat', highlightbackground='#ff8c00', highlightthickness=1,
                                      command=lambda l=label: self.button_press(l))
                    button.grid(row=row + 1, column=col, sticky='nsew', padx=2, pady=2)
                    self.buttons.append(button)

        for i in range(4):
            self.master.columnconfigure(i, weight=1)
        for i in range(8):
            self.master.rowconfigure(i, weight=1)

        self.context_menu = Menu(self.master, tearoff=0, bg=self.current_theme['bg'], fg=self.current_theme['fg'])
        self.context_menu.add_command(label="Toggle Theme", command=self.toggle_theme)
        self.master.bind('<Button-3>', self.show_context_menu)

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def button_press(self, label):
        """Handle button presses, positioning cursor after numbers by default for operators and functions."""
        current = self.display_var.get()
        cursor_pos = self.display.index(tk.INSERT)

        # Remove initial zero for any valid input except decimal point
        if current == "0" and label != '.':
            if label in '0123456789+-*/^()' or label in ['sqrt', 'fact', '1/x', '%', 'pi', '+/-']:
                current = ""
                cursor_pos = 0
        
        # Determine if the label is an operator, function, or parenthesis
        is_operator = label in '+-*/^'
        is_function = label in ['sqrt', 'fact', '1/x', '%']
        is_constant = label == 'pi'

        if label in '0123456789.':  # Digits and decimal point
            # Find if we're inside a negative number
            before_cursor = current[:cursor_pos]
            neg_number_match = re.search(r'-\d*$', before_cursor)
            
            new_text = current[:cursor_pos] + label + current[cursor_pos:]
            self.display_var.set(new_text)
            # If we're adding to a negative number, move cursor after the digit
            if neg_number_match:
                self.display.icursor(cursor_pos + 1)
            else:
                self.display.icursor(cursor_pos + 1)
        elif label == 'AC':  # All Clear
            self.display_var.set("0")
            self.display.icursor(0)
        elif label == 'DEL':  # Delete
            if cursor_pos > 0:
                new_text = current[:cursor_pos - 1] + current[cursor_pos:]
                self.display_var.set(new_text if new_text else "0")
                self.display.icursor(cursor_pos - 1)
        elif label == '=':  # Calculate result
            self.calculate()
            self.display.icursor(len(self.display_var.get()))
        elif is_operator:
            # Find the last number or expression end and place cursor after it
            last_number_match = re.search(r'[-+]?\d+\.?\d*$', current[:cursor_pos])
            if last_number_match:
                start_pos = last_number_match.start()
                new_text = current[:cursor_pos] + label + current[cursor_pos:]
                self.display_var.set(new_text)
                self.display.icursor(cursor_pos + len(label) + (cursor_pos - start_pos))
            else:
                new_text = current[:cursor_pos] + label + current[cursor_pos:]
                self.display_var.set(new_text)
                self.display.icursor(cursor_pos + len(label))
        elif is_function:
            self.handle_function(label, current, cursor_pos)
        elif is_constant:
            # Insert 'pi' as a constant, not a function
            new_text = current[:cursor_pos] + 'pi' + current[cursor_pos:]
            self.display_var.set(new_text)
            self.display.icursor(cursor_pos + 2)  # After 'pi'
        elif label in '()':  # Parentheses
            new_text = current[:cursor_pos] + label + current[cursor_pos:]
            self.display_var.set(new_text)
            self.display.icursor(cursor_pos + 1)
        elif label == '+/-':  # Sign toggle
            self.handle_sign_toggle(current, cursor_pos)

    def handle_function(self, func, current, cursor_pos):
        """Handle functions like sqrt, fact, 1/x, %, positioning cursor appropriately."""
        before_cursor = current[:cursor_pos]
        number_match = re.search(r'([-]?\d+\.?\d*)$', before_cursor)

        if number_match:
            number = number_match.group(1)
            start_pos = cursor_pos - len(number)
            if func == 'fact':
                try:
                    num_val = float(number)
                    if num_val < 0 or not num_val.is_integer():
                        self.display_var.set("Error: Factorial undefined")
                        return
                    if num_val == 0:
                        new_text = current[:start_pos] + '1' + current[cursor_pos:]
                        self.display_var.set(new_text)
                        self.display.icursor(start_pos + 1)
                        return
                except ValueError:
                    self.display_var.set("Error: Invalid input for factorial")
                    return
            elif func == '1/x':
                new_text = current[:start_pos] + f"1/{number}" + current[cursor_pos:]
                self.display_var.set(new_text)
                self.display.icursor(start_pos + 2 + len(number))  # After the fraction
                return
            new_text = current[:start_pos] + f"{func}({number})" + current[cursor_pos:]
            self.display_var.set(new_text)
            self.display.icursor(start_pos + len(func) + len(number) + 2)  # After the closing parenthesis
        else:
            if func == '1/x':
                new_text = current[:cursor_pos] + "1/" + current[cursor_pos:]
                self.display_var.set(new_text)
                self.display.icursor(cursor_pos + 2)  # After '/'
            else:
                new_text = current[:cursor_pos] + f"{func}()" + current[cursor_pos:]
                self.display_var.set(new_text)
                self.display.icursor(cursor_pos + len(func) + 1)  # Inside parentheses for immediate input

    def handle_sign_toggle(self, current, cursor_pos):
        """Toggle the sign of the number before the cursor or insert '-' if appropriate."""
        before_cursor = current[:cursor_pos]
        after_cursor = current[cursor_pos:]
        number_match = re.search(r'([-]?\d+\.?\d*)$', before_cursor)

        if number_match:
            number = number_match.group(1)
            start_pos = cursor_pos - len(number)
            if number.startswith('-'):
                new_number = number[1:]
                new_cursor_pos = start_pos + len(new_number)
            else:
                new_number = '-' + number
                new_cursor_pos = start_pos + len(new_number)
            new_text = current[:start_pos] + new_number + after_cursor
            self.display_var.set(new_text)
            self.display.icursor(new_cursor_pos)  # Place cursor after the entire number
        else:
            # Insert '-' if at the start or after an operator/parenthesis
            if cursor_pos == 0 or (cursor_pos > 0 and current[cursor_pos - 1] in '+-*/^('):
                new_text = current[:cursor_pos] + '-' + current[cursor_pos:]
                self.display_var.set(new_text)
                self.display.icursor(cursor_pos + 1)
            else:
                # If no number and not at a valid position, do nothing
                pass

    def calculate(self):
        """Evaluate the expression and display the result."""
        expr = self.display_var.get()
        expr = re.sub(r'(-?\d+\.?\d*)\s*\^\s*(-?\d+\.?\d*)', r'(\1)**(\2)', expr)
        expr = expr.replace('^', '**')
        expr = re.sub(r'(\d+(?:\.\d+)?|\([^\)]+\))!', r'fact(\1)', expr)
        try:
            result = eval(expr, {'__builtins__': {}}, 
                         {'sqrt': math.sqrt, 'pi': math.pi, 'fact': math.factorial})
            self.display_var.set(str(result))
        except Exception as e:
            self.display_var.set("Error: " + str(e))

    def toggle_theme(self):
        if self.theme == "dark":
            self.theme = "light"
            self.current_theme = self.light_theme
        else:
            self.theme = "dark"
            self.current_theme = self.dark_theme

        self.master.config(bg=self.current_theme['bg'])
        self.display.config(bg='#000000' if self.theme == "dark" else '#ffffff', 
                           fg='#ffffff' if self.theme == "dark" else '#000000',
                           insertbackground='#ffffff' if self.theme == "dark" else '#000000')
        for button in self.buttons:
            button.config(bg=self.current_theme['button_bg'], fg=self.current_theme['button_fg'])

if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()