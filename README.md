# Interactive Numerical Calculus Learning Tool 🧮

An interactive desktop application built with Python to help students visualize and understand fundamental concepts of numerical calculus. The tool provides hands-on demonstrations of error analysis, root-finding methods, linear systems, interpolation, curve fitting, and numerical integration, all within a modern, user-friendly interface.

-----

## Features ✨

The application is organized into six main modules, targeting core areas of numerical calculus.

### **1. Noções de Erro (Notions of Error) 🎓**
* **Floating-Point Analysis:** Input any decimal number and see its binary representation according to the **IEEE 754 standard** (32-bit and 64-bit). Break down the sign, exponent, and mantissa to visualize representation errors.
* **Truncation Error Visualization:** Approximate functions like $sin(x)$, $cos(x)$, and $e^x$ using Taylor series. Interactively change the number of terms and observe the absolute and relative errors alongside a visual plot.

### **2. Zeros de Funções (Zeros of Functions) 🎯**
* **Bisection Method:** Step-by-step iteration table and visualization of the interval converging on the root.
* **Newton-Raphson Method:** Symbolic derivative computation, iteration table, and tangent line visualization at each step.

### **3. Sistemas Lineares (Linear Systems) 🔢**
* **Gaussian Elimination:** Dynamic grid input to demonstrate forward elimination (with partial pivoting) and back substitution.
* **Ill-Conditioned Systems:** Analyze sensitivity using Hilbert matrices and condition numbers.
* **Gauss-Seidel Method:** Iterative solution visualization (functionality pending implementation details).

### **4. Interpolação (Interpolation) 📈**
* **Lagrange Polynomial:** Input a set of points $(x, y)$ to generate the exact interpolating polynomial $P_n(x)$.
* **Estimation:** Calculate $y$ for any specific $x$ using the generated polynomial.
* **Visualization:** Plots the original points and the resulting polynomial curve to demonstrate the fit.

### **5. Mínimos Quadrados (Least Squares) 📉**
* **Multiple Regression Models:**
    * Linear ($y = ax + b$)
    * Polynomial (User-defined degree)
    * Exponential ($y = ae^{bx}$, linearized)
    * Fourier Series (Discrete trigonometric approximation)
* **Didactic Output:** Displays the intermediate **Design Matrix (A)** and the **Normal Equations** matrix ($A^T A$) before solving for coefficients.
* **Analysis:** Calculates the Total Squared Error and overlays the fitted curve on the scatter plot of experimental data.

### **6. Integração Numérica (Numerical Integration) ∫**
* **Newton-Cotes Rules:**
    * Trapezoidal Rule
    * Simpson's 1/3 Rule
    * Simpson's 3/8 Rule
* **Gauss Quadrature:** Gaussian-Legendre integration for 2, 3, and 4 points with variable mapping visualization.
* **Error Analysis:** Compares the numerical result against the **exact symbolic integral** (using SymPy) to display the precise absolute error.
* **Visualization:** Visualizes the area under the curve and the approximation shapes (trapezoids/rectangles).

-----

## Tech Stack 💻

* **Language:** Python 3
* **GUI:** CustomTkinter
* **Numerical Operations:** NumPy, SciPy
* **Plotting:** Matplotlib
* **Symbolic Mathematics:** SymPy

-----

## Installation & Setup 🚀

**Prerequisites:**
* Python 3.8 or newer
* `pip` and `venv`

**Steps:**

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/CalculusTool.git](https://github.com/your-username/CalculusTool.git)
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
    *(Note: Ensure `scipy` is included in your requirements.txt)*

-----

## Usage

Run the application from the root directory:

```bash
python main.py
```
-----
## Structure
/CalculusTool/
|
├── main.py                     # Main entry point
├── app.py                      # Main App class & navigation logic
├── requirements.txt            # Project dependencies
|
├── gui/                        # GUI modules for each section
│   ├── error_frame.py          # Floating point & Truncation
│   ├── zeros_frames.py         # Bisection & Newton-Raphson
│   ├── linear_systems_frame.py # Gaussian Elimination
│   ├── interpolation_frame.py  # Lagrange Interpolation
│   ├── least_squares_frame.py  # Curve Fitting (MMQ)
│   └── integration_frame.py    # Numerical Integration
|
└── utils/                      # Helper modules
    └── ieee754_converter.py    # Binary representation logic

  ## License
  
This project is licensed under the MIT License. See the LICENSE file for details.
