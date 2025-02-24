import tkinter as tk
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
        self.display.focus_set()

        # Keyboard bindings
        self.display.bind('<Key>', self.handle_keyboard_input)
        self.master.bind('<Return>', lambda e: self.button_press('='))
        self.master.bind('<KP_Enter>', lambda e: self.button_press('='))
        self.master.bind('<Escape>', lambda e: self.button_press('AC'))
        self.master.bind('<Delete>', lambda e: self.button_press('AC'))
        self.master.bind('<BackSpace>', lambda e: self.button_press('DEL'))
        self.master.bind('<F1>', lambda e: self.button_press('sqrt'))
        self.master.bind('<F2>', lambda e: self.button_press('fact'))
        self.master.bind('<F3>', lambda e: self.button_press('1/x'))
        self.master.bind('<F4>', lambda e: self.button_press('+/-'))
        self.master.bind('<F5>', lambda e: self.button_press('pi'))
        self.master.bind('<F12>', lambda e: self.toggle_theme())

        # Numpad bindings
        numpad_keys = ['<KP_0>', '<KP_1>', '<KP_2>', '<KP_3>', '<KP_4>',
                       '<KP_5>', '<KP_6>', '<KP_7>', '<KP_8>', '<KP_9>',
                       '<KP_Add>', '<KP_Subtract>', '<KP_Multiply>', 
                       '<KP_Divide>', '<KP_Decimal>']
        for key in numpad_keys:
            self.master.bind(key, lambda e, k=key: self.handle_numpad(k))

        # Button layout
        buttons_layout = [
            ['AC', 'DEL', '%', '+'],
            ['7', '8', '9', '-'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '/'],
            ['0', '.', '=', 'sqrt'],
            ['fact', 'pi', '(', ')'],
            ['1/x', '^', '+/-', '']
        ]
        self.create_buttons(buttons_layout)

        # Grid configuration
        for i in range(4):
            self.master.columnconfigure(i, weight=1)
        for i in range(8):
            self.master.rowconfigure(i, weight=1)

        # Context menu (Fixed: Use tk.Menu instead of Menu)
        self.context_menu = tk.Menu(self.master, tearoff=0, bg=self.current_theme['bg'], fg=self.current_theme['fg'])
        self.context_menu.add_command(label="Toggle Theme", command=self.toggle_theme)
        self.master.bind('<Button-3>', self.show_context_menu)

    def create_buttons(self, buttons_layout):
        """Create and grid calculator buttons."""
        self.buttons = []
        for row in range(len(buttons_layout)):
            for col in range(4):
                label = buttons_layout[row][col]
                if label:
                    button = tk.Button(self.master, text=label, font=('Arial', 14, 'bold'), width=7, height=2,
                                      bg=self.current_theme['button_bg'], fg=self.current_theme['button_fg'],
                                      relief='flat', highlightbackground='#ff8c00', highlightthickness=1,
                                      command=lambda l=label: self.button_press(l))
                    button.grid(row=row + 1, column=col, sticky='nsew', padx=2, pady=2)
                    self.buttons.append(button)

    def show_context_menu(self, event):
        """Display the right-click context menu."""
        self.context_menu.post(event.x_root, event.y_root)

    def handle_numpad(self, key):
        """Handle numpad key presses."""
        numpad_map = {
            '<KP_0>': '0', '<KP_1>': '1', '<KP_2>': '2', '<KP_3>': '3',
            '<KP_4>': '4', '<KP_5>': '5', '<KP_6>': '6', '<KP_7>': '7',
            '<KP_8>': '8', '<KP_9>': '9', '<KP_Add>': '+', 
            '<KP_Subtract>': '-', '<KP_Multiply>': '*', '<KP_Divide>': '/',
            '<KP_Decimal>': '.'
        }
        self.button_press(numpad_map[key])

    def handle_keyboard_input(self, event):
        """Handle keyboard input with simplified mappings."""
        char = event.char
        keysym = event.keysym

        # Allow cursor movement without interference
        if keysym in ['Left', 'Right']:
            return

        # Prevent default Entry widget behavior
        if keysym not in ['Left', 'Right']:
            event.widget.tk_focusNext().focus()
            event.widget.focus_set()

        key_mapping = {
            '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
            '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
            '+': '+', '-': '-', '*': '*', '/': '/',
            '.': '.', '(': '(', ')': ')', '^': '^', '%': '%',
            's': 'sqrt', 'f': 'fact', 'i': '1/x', 'p': 'pi', 
            'n': '+/-', 't': 'AC', 'd': 'DEL',
            '\r': '=', '\x08': 'DEL', '\x1b': 'AC'
        }

        shift_mapping = {
            '8': '*', '6': '^', '5': '%'
        }

        ctrl_mapping = {
            'z': 'DEL', 'c': 'AC', 'r': '1/x', 'q': 'sqrt'
        }

        if event.state & 0x4 and char in ctrl_mapping:  # Ctrl pressed
            self.button_press(ctrl_mapping[char.lower()])
        elif event.state & 0x1 and char in shift_mapping:  # Shift pressed
            self.button_press(shift_mapping[char])
        elif char in key_mapping:
            self.button_press(key_mapping[char])
        else:
            return 'break'
        return 'break'

    def set_cursor_position(self, position):
        """Centralized cursor positioning method."""
        try:
            self.display.icursor(position)
        except tk.TclError:
            self.display.icursor(len(self.display_var.get()))

    def button_press(self, label):
        """Handle button presses with consistent cursor positioning."""
        cursor_pos = self.display.index(tk.INSERT)
        current = self.display_var.get()

        # Clear initial zero for new input (except decimal)
        if current == "0" and label != '.' and label not in ['AC', 'DEL', '=']:
            current = ""
            cursor_pos = 0

        is_operator = label in '+-*/^'
        is_function = label in ['sqrt', 'fact', '1/x', '%']
        is_constant = label == 'pi'

        if label in '0123456789.':
            new_text = current[:cursor_pos] + label + current[cursor_pos:]
            self.display_var.set(new_text)
            self.set_cursor_position(cursor_pos + 1)
        elif label == 'AC':
            self.display_var.set("0")
            self.set_cursor_position(0)
        elif label == 'DEL':
            if cursor_pos > 0:
                new_text = current[:cursor_pos - 1] + current[cursor_pos:]
                self.display_var.set(new_text if new_text else "0")
                self.set_cursor_position(cursor_pos - 1)
        elif label == '=':
            self.calculate()
            self.set_cursor_position(len(self.display_var.get()))
        elif is_operator:
            new_text = current[:cursor_pos] + label + current[cursor_pos:]
            self.display_var.set(new_text)
            self.set_cursor_position(cursor_pos + 1)
        elif is_function:
            self.handle_function(label, current, cursor_pos)
        elif is_constant:
            new_text = current[:cursor_pos] + 'pi' + current[cursor_pos:]
            self.display_var.set(new_text)
            self.set_cursor_position(cursor_pos + 2)
        elif label in '()':
            new_text = current[:cursor_pos] + label + current[cursor_pos:]
            self.display_var.set(new_text)
            self.set_cursor_position(cursor_pos + 1)
        elif label == '+/-':
            self.handle_sign_toggle(current, cursor_pos)

    def handle_function(self, func, current, cursor_pos):
        """Handle mathematical functions with proper cursor positioning."""
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
                        self.set_cursor_position(start_pos + 1)
                        return
                except ValueError:
                    self.display_var.set("Error: Invalid input for factorial")
                    return
            elif func == '1/x':
                new_text = current[:start_pos] + f"1/{number}" + current[cursor_pos:]
                self.display_var.set(new_text)
                self.set_cursor_position(start_pos + 2 + len(number))
                return
            new_text = current[:start_pos] + f"{func}({number})" + current[cursor_pos:]
            self.display_var.set(new_text)
            self.set_cursor_position(start_pos + len(func) + len(number) + 2)
        else:
            if func == '1/x':
                new_text = current[:cursor_pos] + "1/" + current[cursor_pos:]
                self.display_var.set(new_text)
                self.set_cursor_position(cursor_pos + 2)
            else:
                new_text = current[:cursor_pos] + f"{func}()" + current[cursor_pos:]
                self.display_var.set(new_text)
                self.set_cursor_position(cursor_pos + len(func) + 1)

    def handle_sign_toggle(self, current, cursor_pos):
        """Toggle the sign of the number before the cursor."""
        before_cursor = current[:cursor_pos]
        after_cursor = current[cursor_pos:]
        number_match = re.search(r'([-]?\d+\.?\d*)$', before_cursor)

        if number_match:
            number = number_match.group(1)
            start_pos = cursor_pos - len(number)
            new_number = number[1:] if number.startswith('-') else '-' + number
            new_text = current[:start_pos] + new_number + after_cursor
            self.display_var.set(new_text)
            self.set_cursor_position(start_pos + len(new_number))
        elif cursor_pos == 0 or (cursor_pos > 0 and current[cursor_pos - 1] in '+-*/^('):
            new_text = current[:cursor_pos] + '-' + current[cursor_pos:]
            self.display_var.set(new_text)
            self.set_cursor_position(cursor_pos + 1)

    def calculate(self):
        """Evaluate the expression with improved error handling."""
        expr = self.display_var.get()
        expr = re.sub(r'(-?\d+\.?\d*)\s*\^\s*(-?\d+\.?\d*)', r'(\1)**(\2)', expr)
        expr = expr.replace('^', '**')
        expr = re.sub(r'(\d+(?:\.\d+)?|\([^\)]+\))!', r'fact(\1)', expr)
        expr = re.sub(r'(\d+|\))\s*\(', r'\1*(', expr)  # Implicit multiplication
        
        try:
            result = eval(expr, {'__builtins__': {}}, 
                         {'sqrt': math.sqrt, 'pi': math.pi, 'fact': math.factorial})
            self.display_var.set(str(result))
        except ZeroDivisionError:
            self.display_var.set("Error: Division by zero")
        except OverflowError:
            self.display_var.set("Error: Result too large")
        except ValueError:
            self.display_var.set("Error: Invalid input")
        except Exception:
            self.display_var.set("Error: Invalid expression")

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        self.theme = "light" if self.theme == "dark" else "dark"
        self.current_theme = self.light_theme if self.theme == "light" else self.dark_theme

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