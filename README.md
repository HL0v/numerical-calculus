<<<<<<< HEAD
Of course. Here is a complete `README.md` file for the application.

-----

# Interactive Numerical Calculus Learning Tool 🧮

An interactive desktop application built with Python to help students visualize and understand fundamental concepts of numerical calculus. The tool provides hands-on demonstrations of error analysis, root-finding methods, and techniques for solving linear systems, all within a modern, user-friendly interface.

-----

## Features ✨

The application is organized into three main modules, each targeting a core area of numerical calculus.

### **1. Noções de Erro (Notions of Error) 🎓**

  * **Floating-Point Analysis:** Input any decimal number and see its binary representation according to the **IEEE 754 standard** for both single (32-bit) and double (64-bit) precision. The tool breaks down the representation into its sign, exponent, and mantissa, and shows the actual decimal value stored to highlight representation errors.
  * **Truncation Error Visualization:** See how a Taylor series approximates functions like $sin(x)$, $cos(x)$, and $e^x$. Interactively change the number of terms and see the approximation, errors (absolute and relative), and a plot comparing the real function to its polynomial approximation.

-----

### **2. Zeros de Funções (Zeros of Functions) 🎯**

  * **Bisection Method:** Input a function, an interval $[a, b]$, and a tolerance. The tool provides a step-by-step table of iterations and visually plots the function, highlighting how the interval converges on the root at each step.
  * **Newton-Raphson Method:** Input a function and an initial guess. The application symbolically computes the derivative, displays a detailed iteration table, and plots the function along with the **tangent line** at each step to show how the next approximation is found.

-----

### **3. Sistemas Lineares (Linear Systems) 🔢**

  * **Gaussian Elimination:** Enter a matrix `A` and vector `b` into a dynamic grid. The tool demonstrates the step-by-step process of forward elimination (with optional **partial pivoting**) and back substitution to find the solution vector `x`.
  * **Ill-Conditioned Systems:** Load a classic ill-conditioned system (like a Hilbert matrix) to understand sensitivity. Make a tiny change in the vector `b` and observe the dramatic change in the solution `x`, reinforced by the calculated **condition number**.
  * **Gauss-Seidel Method:** Solve systems iteratively. The tool checks for diagonal dominance and shows the solution vector converging at each step until the desired tolerance is met.

-----

## Tech Stack 💻

  * **Language:** Python 3
  * **GUI:** CustomTkinter
  * **Numerical Operations:** NumPy
  * **Plotting:** Matplotlib
  * **Symbolic Mathematics:** SymPy

-----

## Installation & Setup 🚀

To get the application running on your local machine, follow these simple steps.

**Prerequisites:**

  * Python 3.8 or newer
  * `pip` and `venv`

**Steps:**

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/CalculusTool.git
    cd CalculusTool
    ```

2.  **Create and activate a virtual environment:**

      * **Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
      * **macOS / Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

-----

## Usage

Once the setup is complete, run the application from the root directory:

```bash
python main.py
```

-----

## File Structure

The project is organized into modules for better maintainability:

```
/CalculusTool/
|
├── main.py                     # Main entry point to run the application
├── app.py                      # The main App class (window, sidebar, frame management)
├── requirements.txt            # Project dependencies
|
├── gui/                        # GUI modules for each section
│   ├── error_frame.py
│   ├── zeros_frame.py
│   └── linear_systems_frame.py
|
└── utils/                      # Helper modules and backend logic
    └── ieee754_converter.py
```

-----

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
=======
