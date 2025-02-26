# Advanced Calculator Application

A feature-rich calculator built with Python and Tkinter that offers a user-friendly interface with advanced mathematical functions, calculation history, memory operations, and theme customization.

## Features

### Core Functionality
- Basic arithmetic operations: addition, subtraction, multiplication, and division
- Advanced mathematical functions: square root, factorial, reciprocal (1/x)
- Support for parentheses and order of operations
- Percentage calculations
- Exponential operations using the ^ symbol

### User Interface
- Clean, modern interface with dark and light themes
- Two-display system showing current input and previous calculations
- Keyboard and numpad support for all operations
- Customizable through right-click context menu

### Memory Operations
- MC (Memory Clear): Reset the memory value
- MR (Memory Recall): Display the current memory value
- M+ (Memory Add): Add the current display value to memory
- M- (Memory Subtract): Subtract the current display value from memory

### History System
- Track calculation history throughout the session
- Navigate through previous calculations using arrow keys
- Access full history through the dedicated "Hist" button
- Double-click history items to reuse them

### Clipboard Integration
- Copy current display value to clipboard
- Paste numeric values from clipboard into the calculator
- Smart filtering for non-numeric content

### Keyboard Shortcuts
- Enter/Return: Calculate result
- Escape/Delete: Clear All (AC)
- Backspace: Delete last character (DEL)
- F1-F5: Various mathematical functions
- F12: Toggle theme
- Up/Down arrows: Navigate history
- Ctrl+H: Show history dialog

## Requirements
- Python 3.x
- Tkinter (usually included with Python)

## Installation

1. Ensure Python 3.x is installed on your system
2. Clone or download this repository
3. Run the calculator:

```bash
python calculator.py
```

## Usage Examples

### Basic Calculations
- Enter numbers and operators using the keypad or keyboard
- Press = or Enter to calculate the result

### Using Advanced Functions
- For square root: Press the sqrt button or F1, then enter a number, e.g., `sqrt(25)`
- For factorial: Enter a number, then press the fact button or F2, e.g., `5!`
- For reciprocal: Enter a number, then press 1/x or F3, e.g., `1/5`

### Working with Memory
- Calculate a value, then press M+ to add it to memory
- Press MR to recall the memory value into the display
- Use M- to subtract the current value from memory
- Press MC to clear the memory

### Using History
- Navigate through calculation history with Up/Down arrow keys
- Click the "Hist" button (or press Ctrl+H) to see full calculation history
- Double-click any history item to use it again

## Customization

### Changing Themes
- Use F12 or right-click and select "Toggle Theme" to switch between light and dark modes
- The calculator will maintain your theme preference during the session

## Error Handling

The calculator provides specific error messages for various situations:
- "Error: Division by zero" when attempting to divide by zero
- "Error: Result too large" for calculations resulting in overflow
- "Error: Invalid input" for malformed expressions
- "Error: Factorial undefined" when attempting factorial of negative or non-integer values
- "Error: Cannot sqrt negative number" when attempting to find the square root of a negative number

## Contributing

Contributions to improve the calculator are welcome:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is released under the MIT License - see the LICENSE file for details.