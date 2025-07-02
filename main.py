import tkinter as tk
import math
import re

print("--- Program Start ---")

class Calculator:
    def __init__(self, master):
        print("Calculator: __init__ started")
        self.master = master
        self.master.title("Scientific Calculator")
        self.master.geometry("400x550")  # Slightly taller to accommodate UI improvements

        # Theme setup
        self.theme = "dark"
        self.themes = {
            "light": {
                'bg': 'white',
                'fg': 'black',
                'button_bg': '#f0f0f0',
                'button_fg': '#0066cc',
                'equals_bg': '#007acc',
                'equals_fg': 'white',
                'clear_bg': '#d32f2f',
                'clear_fg': 'white',
                'operator_bg': '#dddddd',
                'operator_fg': '#0066cc',
                'function_bg': '#e6e6e6',
                'function_fg': '#0066cc',
                'memory_bg': '#008844',
                'memory_fg': 'white',
                'display_bg': '#ffffff',
                'display_fg': '#000000',
                'display_insert_bg': '#000000',
                'history_label_bg': '#e0e0e0',
            },
            "dark": {
                'bg': '#1a1a1a',
                'fg': 'white',
                'button_bg': '#333333',
                'button_fg': '#00aaff',
                'equals_bg': '#007acc',
                'equals_fg': 'white',
                'clear_bg': '#d32f2f',
                'clear_fg': 'white',
                'operator_bg': '#555555',
                'operator_fg': '#00aaff',
                'function_bg': '#444444',
                'function_fg': '#ffcc00',
                'memory_bg': '#006633',
                'memory_fg': 'white',
                'display_bg': '#000000',
                'display_fg': '#ffffff',
                'display_insert_bg': '#ffffff',
                'history_label_bg': '#121212',
            }
        }
        self.current_theme = self.themes[self.theme]

        # History setup
        self.history = []
        # history_index points to the current item being displayed from history,
        # or len(self.history) if current input is not from history
        self.history_index = 0 

        # Display setup
        self.display_var = tk.StringVar(value="0")
        self.display_frame = tk.Frame(self.master, bg=self.current_theme['bg'], bd=2, relief=tk.RAISED)
        self.display_frame.grid(row=0, column=0, columnspan=4, sticky='nsew', padx=10, pady=10)
        
        # History label
        self.history_var = tk.StringVar(value="")
        self.history_label = tk.Label(self.display_frame, textvariable=self.history_var, font=('Arial', 12), 
                                     bg=self.current_theme['history_label_bg'], fg=self.current_theme['fg'], anchor='e', padx=5, pady=3)
        self.history_label.pack(fill='x', padx=5, pady=(5, 0))
        
        # Main display
        self.display = tk.Entry(self.display_frame, textvariable=self.display_var, font=('Arial', 24, 'bold'), justify='right',
                               bg=self.current_theme['display_bg'], fg=self.current_theme['display_fg'], 
                               insertbackground=self.current_theme['display_insert_bg'], relief='flat',
                               bd=10, highlightthickness=1, highlightcolor=self.current_theme['button_fg'])
        self.display.pack(fill='both', expand=True, padx=5, pady=5)
        self.display.focus_set()

        # Keyboard bindings
        # Note: handle_keyboard_input must be defined before this line.
        # Ensure it's part of the class scope and correctly indented.
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
        self.master.bind('<F6>', lambda e: self.button_press('log10'))
        self.master.bind('<F12>', lambda e: self.toggle_theme())
        
        # History navigation
        self.master.bind('<Up>', lambda e: self.navigate_history(-1))
        self.master.bind('<Down>', lambda e: self.navigate_history(1))

        # Numpad bindings
        numpad_keys = {
            '<KP_0>': '0', '<KP_1>': '1', '<KP_2>': '2', '<KP_3>': '3',
            '<KP_4>': '4', '<KP_5>': '5', '<KP_6>': '6', '<KP_7>': '7',
            '<KP_8>': '8', '<KP_9>': '9', '<KP_Add>': '+', 
            '<KP_Subtract>': '-', '<KP_Multiply>': '*', 
            '<KP_Divide>': '/', '<KP_Decimal>': '.'
        }
        for key, value in numpad_keys.items():
            self.master.bind(key, lambda e, v=value: self.button_press(v))

        # Button layout
        buttons_layout = [
            ['AC', 'DEL', 'log10', '+'],
            ['7', '8', '9', '-'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '/'],
            ['0', '.', '=', 'sqrt'],
            ['fact', 'pi', '(', ')'],
            ['1/x', '^', '+/-', 'Hist']
        ]

        # Store the number of rows in the main button layout BEFORE creating buttons
        self.main_button_rows_count = len(buttons_layout)

        # Create button frame for better organization
        self.button_frame = tk.Frame(self.master, bg=self.current_theme['bg'])
        self.button_frame.grid(row=1, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)
        self.master.rowconfigure(1, weight=1)
        
        self.buttons = [] # Store button references for theme changes
        self.create_buttons(buttons_layout)

        # Memory functions
        memory_layout = [['MC', 'MR', 'M+', 'M-']]
        self.memory_value = 0
        self.create_memory_buttons(memory_layout)

        # Grid configuration
        for i in range(4):
            self.master.columnconfigure(i, weight=1)
            self.button_frame.columnconfigure(i, weight=1)
        
        for i in range(self.main_button_rows_count + len(memory_layout)): # For rows in button frame
            self.button_frame.rowconfigure(i, weight=1)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = tk.Label(self.master, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W,
                                  bg=self.current_theme['bg'], fg=self.current_theme['fg'])
        self.status_bar.grid(row=2, column=0, columnspan=4, sticky='ew')

        # Context menu
        self.context_menu = tk.Menu(self.master, tearoff=0, bg=self.current_theme['bg'], fg=self.current_theme['fg'])
        self.context_menu.add_command(label="Toggle Theme", command=self.toggle_theme)
        self.context_menu.add_command(label="Copy", command=self.copy_to_clipboard)
        self.context_menu.add_command(label="Paste", command=self.paste_from_clipboard)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Clear History", command=self.clear_history)
        self.master.bind('<Button-3>', self.show_context_menu)
        
        # Apply initial theme
        print("Calculator: __init__ completed")
        self._apply_theme_to_widgets()
        print("Theme applied")


    def _apply_theme_to_widgets(self):
        """Apply the current theme to all widgets."""
        self.master.config(bg=self.current_theme['bg'])
        self.display_frame.config(bg=self.current_theme['bg'])
        self.button_frame.config(bg=self.current_theme['bg'])
        self.history_label.config(bg=self.current_theme['history_label_bg'], fg=self.current_theme['fg'])
        self.display.config(bg=self.current_theme['display_bg'],
                           fg=self.current_theme['display_fg'],
                           insertbackground=self.current_theme['display_insert_bg'],
                           highlightcolor=self.current_theme['button_fg'])
        self.status_bar.config(bg=self.current_theme['bg'], fg=self.current_theme['fg'])
        self.context_menu.config(bg=self.current_theme['bg'], fg=self.current_theme['fg'])
        
        self._apply_theme_to_buttons()

    def _apply_theme_to_buttons(self):
        """Apply the current theme to all calculator and memory buttons."""
        for button in self.buttons:
            text = button.cget('text')
            if text == '=':
                button.config(bg=self.current_theme['equals_bg'], fg=self.current_theme['equals_fg'])
            elif text in ['AC', 'DEL']:
                button.config(bg=self.current_theme['clear_bg'], fg=self.current_theme['clear_fg'])
            elif text in ['MC', 'MR', 'M+', 'M-']:
                button.config(bg=self.current_theme['memory_bg'], fg=self.current_theme['memory_fg'])
            elif text in ['+', '-', '*', '/', '^']:
                button.config(bg=self.current_theme['operator_bg'], fg=self.current_theme['operator_fg'])
            elif text in ['sqrt', 'fact', '1/x', 'log10', 'pi']:
                button.config(bg=self.current_theme['function_bg'], fg=self.current_theme['function_fg'])
            else:
                button.config(bg=self.current_theme['button_bg'], fg=self.current_theme['button_fg'])
            
            # Ensure active colors match base colors for consistency
            button.config(activebackground=button.cget('bg'), activeforeground=button.cget('fg'))

    def create_buttons(self, buttons_layout):
        """Create and grid calculator buttons with improved styling."""
        for row_idx, row_buttons in enumerate(buttons_layout):
            for col_idx, label in enumerate(row_buttons):
                if label:
                    button = tk.Button(self.button_frame, text=label, font=('Arial', 14, 'bold'), 
                                      relief='raised', bd=3,
                                      command=lambda l=label: self.button_press(l))
                    button.grid(row=row_idx, column=col_idx, sticky='nsew', padx=2, pady=2)
                    self.buttons.append(button)

    def create_memory_buttons(self, memory_layout):
        """Create memory function buttons with improved styling."""
        for row_idx, row_buttons in enumerate(memory_layout):
            for col_idx, label in enumerate(row_buttons):
                if label:
                    button = tk.Button(self.button_frame, text=label, font=('Arial', 12, 'bold'),
                                      relief='raised', bd=2,
                                      command=lambda l=label: self.memory_function(l))
                    button.grid(row=row_idx + self.main_button_rows_count, column=col_idx, sticky='nsew', padx=2, pady=2)
                    self.buttons.append(button)


    def memory_function(self, operation):
        """Handle memory operations."""
        try:
            current_value_str = self.display_var.get()
            if not current_value_str or current_value_str.startswith("Error"):
                self.status_var.set("No valid number in display for memory operation")
                return

            current_value = float(current_value_str)
            if operation == "MC":  # Memory Clear
                self.memory_value = 0
                self.status_var.set("Memory cleared")
            elif operation == "MR":  # Memory Recall
                self.display_var.set(str(self.memory_value))
                self.set_cursor_position(len(str(self.memory_value)))
                self.status_var.set(f"Memory recalled: {self.memory_value}")
            elif operation == "M+":  # Memory Add
                self.memory_value += current_value
                self.status_var.set(f"Added {current_value} to memory. Total: {self.memory_value}")
            elif operation == "M-":  # Memory Subtract
                self.memory_value -= current_value
                self.status_var.set(f"Subtracted {current_value} from memory. Total: {self.memory_value}")
        except ValueError:
            self.display_var.set("Error: Invalid number")
            self.status_var.set("Error: Invalid number for memory operation")
        except Exception as e:
            self.display_var.set("Error in memory operation")
            self.status_var.set(f"Error in memory operation: {e}")

    def show_context_menu(self, event):
        """Display the right-click context menu."""
        self.context_menu.post(event.x_root, event.y_root)

    def copy_to_clipboard(self):
        """Copy display content to clipboard."""
        self.master.clipboard_clear()
        self.master.clipboard_append(self.display_var.get())
        self.status_var.set("Copied display value")

    def paste_from_clipboard(self):
        """Paste clipboard content to display."""
        try:
            clipboard_text = self.master.clipboard_get()
            # Allow only numeric and operator characters
            filtered_text = re.sub(r'[^0-9.+\-*/()^]', '', clipboard_text)
            if filtered_text:
                cursor_pos = self.display.index(tk.INSERT)
                current = self.display_var.get()
                new_text = current[:cursor_pos] + filtered_text + current[cursor_pos:]
                self.display_var.set(new_text)
                self.set_cursor_position(cursor_pos + len(filtered_text))
                self.status_var.set("Pasted from clipboard")
        except tk.TclError:
            self.status_var.set("Clipboard is empty or not text")
        except Exception as e:
            self.status_var.set(f"Error pasting: {e}")

    def handle_keyboard_input(self, event):
        """Handle keyboard input with simplified mappings and prevent default Entry behavior."""
        char = event.char
        keysym = event.keysym

        # Allow cursor movement without interference from 'break'
        if keysym in ['Left', 'Right']:
            return

        # Prevent default Entry widget behavior for most keys by returning 'break'
        # The specific button_press will handle the display update
        
        key_mapping = {
            '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
            '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
            '+': '+', '-': '-', '*': '*', '/': '/',
            '.': '.', '(': '(', ')': ')', '^': '^', 
            's': 'sqrt', 'f': 'fact', 'i': '1/x', 'p': 'pi', 
            'n': '+/-', 'l': 'log10',
        }

        shift_mapping = {
            '8': '*', '6': '^' # Shift+8 for *, Shift+6 for ^
        }

        ctrl_mapping = {
            'h': 'Hist', # Ctrl+H for History
        }
        
        # Check for Ctrl combinations first
        if event.state & 0x4 and char.lower() in ctrl_mapping:  # Ctrl pressed
            self.button_press(ctrl_mapping[char.lower()])
            return 'break'
        # Check for Shift combinations
        elif event.state & 0x1 and keysym in shift_mapping:  # Shift pressed
            self.button_press(shift_mapping[keysym])
            return 'break'
        # Check for regular key presses
        elif char in key_mapping:
            self.button_press(key_mapping[char])
            return 'break'
        
        # For any other key that isn't explicitly handled, prevent default
        # behavior to keep display under calculator's control.
        return 'break' 

    def set_cursor_position(self, position):
        """Centralized cursor positioning method."""
        try:
            self.display.icursor(position)
        except tk.TclError:
            # Fallback for out-of-bounds position, put cursor at end
            self.display.icursor(len(self.display_var.get()))

    def button_press(self, label):
        """Handle button presses with consistent cursor positioning."""
        current = self.display_var.get()
        cursor_pos = self.display.index(tk.INSERT)

        # Update status bar
        self.status_var.set(f"'{label}' pressed")

        # Clear initial zero for new input (except decimal or operators)
        if current == "0" and label not in ['.', 'AC', 'DEL', '=', '+/-', 'Hist', '+', '-', '*', '/', '^', '(', ')']:
            current = ""
            cursor_pos = 0
            
        # Reset history index if new input is being typed
        if self.history_index != len(self.history):
            self.history_index = len(self.history)
            self.history_var.set("") # Clear history display if new input starts

        is_operator = label in '+-*/^'
        is_function = label in ['sqrt', 'fact', '1/x', 'log10']
        is_constant = label == 'pi'

        if label in '0123456789.':
            new_text = current[:cursor_pos] + label + current[cursor_pos:]
            self.display_var.set(new_text)
            self.set_cursor_position(cursor_pos + 1)
        elif label == 'AC':
            self.display_var.set("0")
            self.history_var.set("")
            self.history_index = 0 # Reset history index
            self.set_cursor_position(1)
            self.status_var.set("Calculator cleared")
        elif label == 'DEL':
            if cursor_pos > 0:
                new_text = current[:cursor_pos - 1] + current[cursor_pos:]
                self.display_var.set(new_text if new_text else "0")
                self.set_cursor_position(cursor_pos - 1)
                self.status_var.set("Last char deleted")
            else:
                self.status_var.set("Nothing to delete")
        elif label == '=':
            self.calculate()
            self.set_cursor_position(len(self.display_var.get()))
        elif is_operator:
            # Prevent multiple operators in a row (except for leading minus)
            if current and current[cursor_pos-1] in '+-*/^' and label in '+-*/^' and cursor_pos > 0:
                new_text = current[:cursor_pos-1] + label + current[cursor_pos:]
                self.display_var.set(new_text)
                self.set_cursor_position(cursor_pos)
            else:
                new_text = current[:cursor_pos] + label + current[cursor_pos:]
                self.display_var.set(new_text)
                self.set_cursor_position(cursor_pos + 1)
        elif is_function:
            self.handle_function(label, current, cursor_pos)
        elif is_constant:
            pi_str = str(math.pi)
            new_text = current[:cursor_pos] + pi_str + current[cursor_pos:]
            self.display_var.set(new_text)
            self.set_cursor_position(cursor_pos + len(pi_str))
        elif label in '()':
            new_text = current[:cursor_pos] + label + current[cursor_pos:]
            self.display_var.set(new_text)
            self.set_cursor_position(cursor_pos + 1)
        elif label == '+/-':
            self.handle_sign_toggle(current, cursor_pos)
        elif label == 'Hist':
            self.show_history_dialog()

    def handle_function(self, func, current, cursor_pos):
        """Handle mathematical functions with proper cursor positioning."""
        before_cursor = current[:cursor_pos]
        after_cursor = current[cursor_pos:]
        number_match = re.search(r'([-]?\d+\.?\d*)$', before_cursor)

        if func == '1/x':
            if number_match:
                number = number_match.group(1)
                start_pos = cursor_pos - len(number)
                try:
                    num_val = float(number)
                    if num_val == 0:
                        self.display_var.set("Error: Division by zero")
                        self.status_var.set("Error: Division by zero")
                        return
                    new_text = current[:start_pos] + f"1/{number}" + after_cursor
                    self.display_var.set(new_text)
                    self.set_cursor_position(start_pos + 2 + len(number))
                except ValueError:
                    self.display_var.set("Error: Invalid input")
                    self.status_var.set("Error: Invalid input for 1/x")
            else:
                new_text = current[:cursor_pos] + "1/" + after_cursor
                self.display_var.set(new_text)
                self.set_cursor_position(cursor_pos + 2)
        else: # For sqrt, fact, log10
            if number_match:
                number = number_match.group(1)
                start_pos = cursor_pos - len(number)
                
                # Function-specific validation
                if func == 'fact':
                    try:
                        num_val = float(number)
                        if num_val < 0 or not num_val.is_integer():
                            self.display_var.set("Error: Factorial undefined")
                            self.status_var.set("Error: Factorial undefined")
                            return
                        if num_val == 0: # 0! is 1
                            new_text = current[:start_pos] + '1' + after_cursor
                            self.display_var.set(new_text)
                            self.set_cursor_position(start_pos + 1)
                            return
                    except ValueError:
                        self.display_var.set("Error: Invalid input")
                        self.status_var.set("Error: Invalid input for factorial")
                        return
                elif func == 'sqrt':
                    try:
                        num_val = float(number)
                        if num_val < 0:
                            self.display_var.set("Error: Cannot sqrt negative number")
                            self.status_var.set("Error: Cannot sqrt negative number")
                            return
                    except ValueError:
                        self.display_var.set("Error: Invalid input")
                        self.status_var.set("Error: Invalid input for sqrt")
                        return
                elif func == 'log10':
                    try:
                        num_val = float(number)
                        if num_val <= 0:
                            self.display_var.set("Error: Cannot take log of zero or negative")
                            self.status_var.set("Error: Cannot take log of zero or negative")
                            return
                    except ValueError:
                        self.display_var.set("Error: Invalid input")
                        self.status_var.set("Error: Invalid input for log10")
                        return
                    
                new_text = current[:start_pos] + f"{func}({number})" + after_cursor
                self.display_var.set(new_text)
                self.set_cursor_position(start_pos + len(func) + len(number) + 2)
            else:
                new_text = current[:cursor_pos] + f"{func}()" + after_cursor
                self.display_var.set(new_text)
                self.set_cursor_position(cursor_pos + len(func) + 1) # Place cursor inside parentheses

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
            # If at beginning or after an operator/parenthesis, just add a minus sign
            new_text = current[:cursor_pos] + '-' + current[cursor_pos:]
            self.display_var.set(new_text)
            self.set_cursor_position(cursor_pos + 1)
        self.status_var.set("Sign toggled")


    def _validate_expression(self, expr):
        """
        Validates the expression to ensure it only contains allowed characters
        before evaluation. This is a crucial security measure for eval().
        """
        # Allowed characters: digits, operators, parentheses, decimal point, pi (symbol and text), function name characters
        # The regex allows characters that form valid parts of mathematical expressions
        allowed_chars_pattern = r"^[0-9+\-*/().^πa-zA-Z]*$" # Added a-zA-Z for function names

        # Check for disallowed characters first
        if not re.match(allowed_chars_pattern, expr):
            return False, "Error: Invalid characters in expression"

        # Allowed function names that eval can safely call through safe_dict
        # This is a whitelist approach to function names
        allowed_functions = ['sqrt', 'fact', 'sin', 'cos', 'tan', 'log10', 'ln', 'abs', 'pi', 'math']
        
        # Temporarily replace allowed function names to ensure no other alphabetic chars are present
        temp_expr = expr
        for func in allowed_functions:
            temp_expr = temp_expr.replace(func, '') # Remove allowed functions from temp string

        # After removing allowed functions and pi, if there are still alphabetic characters, they are invalid.
        if re.search(r'[a-zA-Z]', temp_expr):
            return False, "Error: Disallowed function or variable name"

        return True, ""


    def calculate(self):
        """Evaluate the expression with improved error handling and safety."""
        expr = self.display_var.get()
        
        # Skip calculation if the expression is already showing an error or is empty
        if not expr or expr.startswith("Error:"):
            return
            
        # Validate expression for allowed characters
        is_valid, error_msg = self._validate_expression(expr)
        if not is_valid:
            self.display_var.set(error_msg)
            self.status_var.set(error_msg)
            return

        # Save expression to history (before processing for display)
        self.history.append(expr)
        
        # Pre-process the expression for eval()
        expr = expr.replace('π', str(math.pi))  # Handle pi symbol
        expr = expr.replace('pi', str(math.pi)) # Handle 'pi' string
        expr = re.sub(r'(\d+)(\s*\*?\s*pi)', r'\1*math.pi', expr) # Handle implicit multiplication with pi, e.g., 2pi, 2*pi
        expr = re.sub(r'(\d+(?:\.\d+)?|\))(\s*\()', r'\1*\2', expr) # Implicit multiplication for numbers/parentheses, e.g., 2(3) -> 2*(3)
        expr = re.sub(r'(\d+(?:\.\d+)?|\))\s*([a-zA-Z_][a-zA-Z0-9_]*)\(', r'\1*\2(', expr) # Implicit multiplication with functions, e.g., 2sqrt(4) -> 2*sqrt(4)
        expr = expr.replace('^', '**') # Convert power symbol
        expr = re.sub(r'(\d+(?:\.\d+)?|\))\s*!', r'math.factorial(\1)', expr) # Convert factorial symbol x! to math.factorial(x)
        
        # Define safe functions for eval
        safe_dict = {
            'sqrt': math.sqrt,
            'pi': math.pi, # Also include pi directly if not replaced as string
            'fact': math.factorial, # Alias fact to math.factorial
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log10': math.log10,
            'ln': math.log,
            'abs': abs,
            'math': math # Allow access to math module for functions like math.pi, math.factorial
        }
        
        try:
            # Use eval with restricted globals and locals for safety
            # __builtins__ is set to an empty dict to prevent access to built-in functions
            result = eval(expr, {"__builtins__": {}}, safe_dict)
            
            # Format result based on type
            if isinstance(result, (int, float)):
                # Round to 10 decimal places to avoid excessive floating point precision
                # and remove trailing zeros/decimal point if integer
                formatted_result = '{:.10f}'.format(result).rstrip('0').rstrip('.')
                if not formatted_result: # Handle case like 0.0 becoming ""
                    formatted_result = "0"
            else:
                formatted_result = str(result) # For unexpected types

            self.display_var.set(formatted_result)
            
            # Add result to history (along with original expression)
            self.history[-1] = f"{self.history[-1]} = {formatted_result}" # Update last history item
            self.history_index = len(self.history) # After calculation, history_index points to end
            
            # Update status bar
            self.status_var.set("Calculation complete")
            self.history_var.set(self.history[-1]) # Show full entry in history label
            
        except ZeroDivisionError:
            self.display_var.set("Error: Division by zero")
            self.status_var.set("Error: Division by zero")
        except OverflowError:
            self.display_var.set("Error: Result too large")
            self.status_var.set("Error: Result too large")
        except ValueError as e:
            self.display_var.set(f"Error: {str(e)}")
            self.status_var.set(f"Error: {str(e)}")
        except SyntaxError:
            self.display_var.set("Error: Invalid expression")
            self.status_var.set("Error: Invalid expression syntax")
        except NameError as e: # Catch cases where undefined names are used
            self.display_var.set("Error: Invalid function/name")
            self.status_var.set(f"Error: Invalid function/name - {e}")
        except TypeError as e: # Catch cases like factorial of float or negative
            self.display_var.set(f"Error: Invalid type for operation")
            self.status_var.set(f"Error: Invalid type for operation - {e}")
        except Exception as e:
            self.display_var.set("Error: Calculation failed")
            self.status_var.set(f"Error: An unexpected error occurred: {e}")

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        self.theme = "light" if self.theme == "dark" else "dark"
        self.current_theme = self.themes[self.theme]
        
        self._apply_theme_to_widgets()
        
        # Update status
        self.status_var.set(f"Theme changed to {self.theme.capitalize()}")
            
    def navigate_history(self, direction):
        """Navigate through calculation history."""
        if not self.history:
            self.status_var.set("History is empty")
            return
        
        # Adjust history_index to point within valid range [0, len(history)-1]
        # or len(history) if at the "new input" state.
        if self.history_index == len(self.history): # Currently at new input state (typing new expression)
            new_index = len(self.history) - 1 # Go to last history item
        else:
            new_index = self.history_index + direction

        if 0 <= new_index < len(self.history):
            self.history_index = new_index
            history_item = self.history[self.history_index]
            
            # Display full history entry in history_var, and result/expression in display_var
            # We assume history items are stored as "expression = result" or just "expression"
            if '=' in history_item:
                parts = history_item.split('=', 1)
                self.history_var.set(parts[0].strip() + " =")
                self.display_var.set(parts[1].strip())
            else: # It's just an expression from a previous input
                self.history_var.set("") # Clear history label if only expression is available
                self.display_var.set(history_item)
            
            self.set_cursor_position(len(self.display_var.get()))
            self.status_var.set(f"History item {self.history_index + 1}/{len(self.history)}")
        elif new_index == len(self.history): # Navigating past last history item (to empty input state)
            self.history_index = len(self.history)
            self.display_var.set("0") # Set display to '0' for new input
            self.history_var.set("") # Clear history label
            self.set_cursor_position(1)
            self.status_var.set("Ready for new input")


    def show_history_dialog(self):
        """Display a dialog with calculation history."""
        history_window = tk.Toplevel(self.master)
        history_window.title("Calculation History")
        history_window.geometry("300x400")
        history_window.configure(bg=self.current_theme['bg'])
        
        history_window.transient(self.master)
        history_window.grab_set()
        
        history_frame = tk.Frame(history_window, bg=self.current_theme['bg'])
        history_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side='right', fill='y')
        
        history_listbox = tk.Listbox(history_frame, bg=self.current_theme['display_bg'], 
                                   fg=self.current_theme['display_fg'],
                                   font=('Arial', 12), selectbackground=self.current_theme['button_fg'], height=15)
        history_listbox.pack(side='left', fill='both', expand=True)
        
        scrollbar.config(command=history_listbox.yview)
        history_listbox.config(yscrollcommand=scrollbar.set)
        
        for item in self.history:
            history_listbox.insert(tk.END, item)
            
        button_frame = tk.Frame(history_window, bg=self.current_theme['bg'])
        button_frame.pack(fill='x', padx=10, pady=5)
            
        def use_selected():
            selected = history_listbox.curselection()
            if selected:
                selected_item = self.history[selected[0]]
                # Distinguish between expression and result for display
                if '=' in selected_item:
                    parts = selected_item.split('=', 1)
                    self.history_var.set(parts[0].strip() + " =")
                    self.display_var.set(parts[1].strip())
                else: # It's just a number (result from previous step)
                    self.history_var.set("") # Clear history label
                    self.display_var.set(selected_item)
                
                self.set_cursor_position(len(self.display_var.get()))
                self.history_index = selected[0] # Update history index to selected item
                history_window.destroy()
                self.status_var.set("History item selected")
                
        use_button = tk.Button(button_frame, text="Use Selected", command=use_selected,
                              bg=self.current_theme['equals_bg'], fg=self.current_theme['equals_fg'], padx=10, pady=5)
        use_button.pack(side='left', padx=5)
        
        def clear_and_close():
            self.clear_history()
            history_window.destroy()
            
        clear_button = tk.Button(button_frame, text="Clear History", command=clear_and_close,
                               bg=self.current_theme['clear_bg'], fg=self.current_theme['clear_fg'], padx=10, pady=5)
        clear_button.pack(side='right', padx=5)
        
        history_listbox.bind('<Double-1>', lambda e: use_selected())
        
    def clear_history(self):
        """Clear calculation history."""
        self.history = []
        self.history_index = 0
        self.history_var.set("")
        self.status_var.set("History cleared")

if __name__ == "__main__":
    print("Creating Tkinter root window...")
    root = tk.Tk()
    print("Tkinter root window created.")
    calc = Calculator(root)
    print("Calculator instance created.")
    print("Starting Tkinter main loop...")
    root.mainloop()
    print("--- Program End ---")