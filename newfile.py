import re
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, messagebox

# 
def sanitize_equation(equation):
    
    equation = equation.replace("^", "**")
    
    equation = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', equation)
    equation = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', equation)
    return equation

# Function to rearrange any given equation into y = ... form
def rearrange_to_y_equals(equation):
    # Define the symbols x and y
    x, y = sp.symbols('x y')

    try:
        # Sanitize the input equation first
        equation = sanitize_equation(equation)
        
        # Convert the string equation to a sympy expression directly
        sympy_eq = sp.sympify(equation)
        
        # Solve the equation for y
        y_expr = sp.solve(sympy_eq, y)
        if not y_expr:
            raise ValueError("No solutions found for y. Make sure your equation involves both x and y.")
        return y_expr[0]  # Return the first solution for y
    except Exception as e:
        raise ValueError(f"Invalid equation format: {e}")

# Function to plot 
def plot_graph(y_expr):
    x_vals = np.linspace(-10, 10, 400)
    f_lambdified = sp.lambdify(sp.symbols('x'), y_expr, 'numpy')
    
    try:
        y_vals = f_lambdified(x_vals)
        plt.plot(x_vals, y_vals, label=f'y = {y_expr}')
        plt.title("Graph of the Equation")
        plt.xlabel("x values")
        plt.ylabel("y values")
        plt.grid(True)
        plt.axhline(0, color='black', linewidth=0.5, ls='--')
        plt.axvline(0, color='black', linewidth=0.5, ls='--')
        plt.legend()
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Error in plotting: {e}")


def on_button_click():
    equation = equation_entry.get()
    try:
        y_expr = rearrange_to_y_equals(equation)
        plot_graph(y_expr)
    except ValueError as e:
        messagebox.showerror("Error", str(e))


root = Tk()
root.title("Universal Equation Plotter")


Label(root, text="Enter the equation involving x and y (e.g., '3*x**2 + y - 5'):").pack()


equation_entry = Entry(root, width=50)
equation_entry.pack()


plot_button = Button(root, text="Plot Grah", command=on_button_click)
plot_button.pack()


root.mainloop()