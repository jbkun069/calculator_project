import tkinter as tk
import math
import re

class Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculator")
        
        # Theme setup
        self.theme = "light"
        self.light_theme = {'bg': 'white', 'fg': 'black'}
        self.dark_theme = {'bg': 'black', 'fg': 'white'}
        self.current_theme = self.light_theme
        
        # Display setup
        self.display_var = tk.StringVar()
        self.display = tk.Entry(self.master, textvariable=self.display_var, font=('Arial', 20), justify='right',
                               bg=self.current_theme['bg'], fg=self.current_theme['fg'],
                               insertbackground=self.current_theme['fg'])
        self.display.grid(row=0, column=0, columnspan=5, sticky='nsew')
        self.display.bind('<Key>', lambda e: 'break')  # Prevent direct keyboard input
        
        # Track cursor position
        self.display.icursor(0)  # Start cursor at beginning
        
        # Button layout
        self.buttons = []
        buttons_layout = [
            ['7', '8', '9', '/', 'sqrt'],
            ['4', '5', '6', '*', 'fact'],
            ['1', '2', '3', '-', 'pi'],
            ['0', '.', '=', '+', '^'],
            ['(', ')', 'C', '<-', 'theme']
        ]
        
        # Create buttons
        for row in range(5):
            for col in range(5):
                label = buttons_layout[row][col]
                button = tk.Button(self.master, text=label, font=('Arial', 15), width=5, height=2,
                                  bg=self.current_theme['bg'], fg=self.current_theme['fg'],
                                  command=lambda l=label: self.button_press(l))
                button.grid(row=row + 1, column=col, sticky='nsew')
                self.buttons.append(button)
        
        # Configure grid to expand
        for i in range(5):
            self.master.columnconfigure(i, weight=1)
        for i in range(6):
            self.master.rowconfigure(i, weight=1)

    def button_press(self, label):
        """Handle button presses."""
        current = self.display_var.get()
        cursor_pos = self.display.index(tk.INSERT)  # Get current cursor position
        
        if label in '0123456789.+-*/^()':  # Digits, operators, power, parentheses
            new_text = current[:cursor_pos] + label + current[cursor_pos:]
            self.display_var.set(new_text)
            self.display.icursor(cursor_pos + 1)
        elif label == 'C':  # Clear all
            self.display_var.set("")
            self.display.icursor(0)
        elif label == '<-':  # Backspace
            if cursor_pos > 0:
                new_text = current[:cursor_pos - 1] + current[cursor_pos:]
                self.display_var.set(new_text)
                self.display.icursor(cursor_pos - 1)
        elif label == '=':  # Calculate result
            self.calculate()
            self.display.icursor(len(self.display_var.get()))
        elif label in ['sqrt', 'fact']:  # Square root or factorial
            self.handle_function(label, current, cursor_pos)
        elif label == 'pi':  # Pi constant
            new_text = current[:cursor_pos] + "pi" + current[cursor_pos:]
            self.display_var.set(new_text)
            self.display.icursor(cursor_pos + 2)
        elif label == 'theme':  # Toggle theme
            self.toggle_theme()

    def handle_function(self, func, current, cursor_pos):
        """Handle sqrt and fact to auto-close brackets and wrap numbers."""
        # Check if there's a number immediately before the cursor
        before_cursor = current[:cursor_pos]
        number_match = re.search(r'(\d+\.?\d*)$', before_cursor)  # Find trailing number
        
        if number_match:  # If a number precedes the cursor
            number = number_match.group(1)
            start_pos = cursor_pos - len(number)
            new_text = current[:start_pos] + f"{func}({number})" + current[cursor_pos:]
            self.display_var.set(new_text)
            self.display.icursor(start_pos + len(func) + len(number) + 2)  # After closing parenthesis
        else:  # No number, insert function with auto-closed brackets
            new_text = current[:cursor_pos] + f"{func}()" + current[cursor_pos:]
            self.display_var.set(new_text)
            self.display.icursor(cursor_pos + len(func) + 1)  # Inside parentheses

    def calculate(self):
        """Evaluate the expression and display the result."""
        expr = self.display_var.get()
        # Preprocess: replace ^ with ** and handle factorial (!)
        expr = expr.replace('^', '**')
        expr = re.sub(r'(\d+(?:\.\d+)?|\([^\)]+\))!', r'fact(\1)', expr)
        try:
            # Safe evaluation with math functions
            result = eval(expr, {'__builtins__': {}}, 
                         {'sqrt': math.sqrt, 'pi': math.pi, 'fact': math.factorial})
            self.display_var.set(str(result))
        except Exception as e:
            self.display_var.set("Error: " + str(e))

    def toggle_theme(self):
        """Switch between light and dark themes."""
        if self.theme == "light":
            self.theme = "dark"
            self.current_theme = self.dark_theme
        else:
            self.theme = "light"
            self.current_theme = self.light_theme
        
        # Update colors
        self.master.config(bg=self.current_theme['bg'])
        self.display.config(bg=self.current_theme['bg'], fg=self.current_theme['fg'],
                           insertbackground=self.current_theme['fg'])
        for button in self.buttons:
            button.config(bg=self.current_theme['bg'], fg=self.current_theme['fg'])

if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()