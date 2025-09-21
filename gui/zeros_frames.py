import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sympy

class ZerosFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Create Tabview for methods
        self.tab_view = ctk.CTkTabview(self, anchor="w")
        self.tab_view.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.tab_view.add("Método da Bissecção")
        self.tab_view.add("Método de Newton-Raphson")

        # Create Plot Frame
        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.plot_frame.grid_rowconfigure(0, weight=1)
        self.plot_frame.grid_columnconfigure(0, weight=1)
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky="nsew")
        self._setup_plot_style()

        # Populate tabs
        self._create_bisection_tab(self.tab_view.tab("Método da Bissecção"))
        self._create_newton_tab(self.tab_view.tab("Método de Newton-Raphson"))

    def _setup_plot_style(self):
        """Sets the dark theme for the Matplotlib plot."""
        self.fig.patch.set_facecolor("#2B2B2B")
        self.ax.set_facecolor("#242424")
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        for spine in self.ax.spines.values():
            spine.set_edgecolor('white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.title.set_color('white')
        self.ax.grid(True, linestyle='--', alpha=0.3, color='gray')
        self.canvas.draw()

    def _create_bisection_tab(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=10)
        
        # --- Inputs ---
        input_frame = ctk.CTkFrame(tab)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(input_frame, text="Função f(x):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.bi_func_entry = ctk.CTkEntry(input_frame, placeholder_text="Ex: x**3 - x - 2")
        self.bi_func_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Intervalo [a, b]:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.bi_a_entry = ctk.CTkEntry(input_frame, placeholder_text="a")
        self.bi_a_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.bi_b_entry = ctk.CTkEntry(input_frame, placeholder_text="b")
        self.bi_b_entry.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Tolerância (ε):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.bi_tol_entry = ctk.CTkEntry(input_frame, placeholder_text="Ex: 0.0001")
        self.bi_tol_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        run_button = ctk.CTkButton(input_frame, text="Calcular", command=self.run_bisection)
        run_button.grid(row=3, column=0, columnspan=3, pady=10)

        # --- Results ---
        self.bi_results_box = ctk.CTkTextbox(tab, wrap="none", font=("Courier", 12))
        self.bi_results_box.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    def _create_newton_tab(self, tab):
        tab.grid_columnconfigure(0, weight=3)
        tab.grid_columnconfigure(1, weight=2)
        
        # --- Inputs ---
        input_frame = ctk.CTkFrame(tab)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(input_frame, text="Função f(x):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.nw_func_entry = ctk.CTkEntry(input_frame, placeholder_text="Ex: x**3 - x - 2")
        self.nw_func_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Chute inicial (x₀):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.nw_x0_entry = ctk.CTkEntry(input_frame, placeholder_text="Ex: 1.0")
        self.nw_x0_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Tolerância (ε):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.nw_tol_entry = ctk.CTkEntry(input_frame, placeholder_text="Ex: 0.0001")
        self.nw_tol_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        run_button = ctk.CTkButton(input_frame, text="Calcular", command=self.run_newton)
        run_button.grid(row=3, column=0, columnspan=2, pady=10)

        # --- Results ---
        self.nw_results_box = ctk.CTkTextbox(tab, wrap="none", font=("Courier", 12))
        self.nw_results_box.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    def _safe_eval_func(self, func_str):
        x = sympy.symbols('x')
        try:
            expr = sympy.sympify(func_str, locals={'e': sympy.E, 'pi': sympy.pi})
            return sympy.lambdify(x, expr, 'numpy')
        except (sympy.SympifyError, SyntaxError):
            return None

    def run_bisection(self):
        try:
            func_str = self.bi_func_entry.get()
            f = self._safe_eval_func(func_str)
            a, b = float(self.bi_a_entry.get()), float(self.bi_b_entry.get())
            tol = float(self.bi_tol_entry.get())
            max_iter = 100

            if f is None or f(a) * f(b) >= 0:
                self.bi_results_box.delete("1.0", "end")
                self.bi_results_box.insert("end", "Erro: Função inválida ou f(a)*f(b) >= 0.")
                return

            results = " n  |      a      |      b      |      c      |     f(c)    |   b-a\n"
            results += "-"*70 + "\n"
            
            self.ax.clear()
            x_plot = np.linspace(min(a, b) - 1, max(a, b) + 1, 400)
            self.ax.plot(x_plot, f(x_plot), label=f'f(x) = {func_str}', color="#007ACC")
            self.ax.axhline(0, color='gray', linewidth=0.5)

            for n in range(max_iter):
                c = (a + b) / 2
                f_c = f(c)
                results += f"{n:2d}  | {a:11.6f} | {b:11.6f} | {c:11.6f} | {f_c:11.6f} | {b-a:11.6f}\n"

                self.ax.axvspan(a, b, alpha=0.1, color='yellow')

                if abs(f_c) < tol or (b - a) / 2 < tol:
                    results += f"\nRaiz encontrada: c = {c}"
                    break
                
                if f(a) * f_c < 0:
                    b = c
                else:
                    a = c
            else:
                results += f"\nMáximo de iterações atingido."
                
            self.bi_results_box.delete("1.0", "end")
            self.bi_results_box.insert("1.0", results)
            
            self.ax.plot(c, f(c), 'ro', label=f'Raiz ≈ {c:.4f}')
            self.ax.legend(facecolor="#2B2B2B", edgecolor="white", labelcolor="white")
            self._setup_plot_style()
        except Exception as e:
            self.bi_results_box.delete("1.0", "end")
            self.bi_results_box.insert("1.0", f"Erro: {e}")

    def run_newton(self):
        try:
            func_str = self.nw_func_entry.get()
            x_sym = sympy.symbols('x')
            expr = sympy.sympify(func_str, locals={'e': sympy.E, 'pi': sympy.pi})
            f = sympy.lambdify(x_sym, expr, 'numpy')
            f_prime_expr = sympy.diff(expr, x_sym)
            f_prime = sympy.lambdify(x_sym, f_prime_expr, 'numpy')

            x0 = float(self.nw_x0_entry.get())
            tol = float(self.nw_tol_entry.get())
            max_iter = 50

            results = " n  |      x_n      |    f(x_n)    |   f'(x_n)   |   |x_n+1 - x_n|\n"
            results += "-"*70 + "\n"
            
            x_n = x0
            
            self.ax.clear()
            x_plot = np.linspace(x0 - 5, x0 + 5, 400)
            self.ax.plot(x_plot, f(x_plot), label=f'f(x) = {func_str}', color="#007ACC")
            self.ax.axhline(0, color='gray', linewidth=0.5)

            for n in range(max_iter):
                f_xn = f(x_n)
                f_prime_xn = f_prime(x_n)
                
                if abs(f_prime_xn) < 1e-12:
                    results += "Derivada próxima de zero. O método falhou."
                    break

                x_n1 = x_n - f_xn / f_prime_xn
                error = abs(x_n1 - x_n)
                
                results += f"{n:2d}  | {x_n:13.8f} | {f_xn:12.8f} | {f_prime_xn:11.8f} | {error:15.8f}\n"

                # Plot tangent line
                tangent_x = np.array([x_n - 1, x_n + 1])
                tangent_y = f_prime_xn * (tangent_x - x_n) + f_xn
                self.ax.plot(tangent_x, tangent_y, '--', color='orange', alpha=0.6)
                self.ax.plot(x_n, f_xn, 'go') # Point on curve
                self.ax.plot(x_n1, 0, 'rx') # Next approximation on x-axis

                if error < tol:
                    results += f"\nRaiz encontrada: x = {x_n1}"
                    x_n = x_n1
                    break
                
                x_n = x_n1
            else:
                results += f"\nMáximo de iterações atingido."

            self.nw_results_box.delete("1.0", "end")
            self.nw_results_box.insert("1.0", results)
            
            self.ax.plot(x_n, f(x_n), 'ro', label=f'Raiz ≈ {x_n:.4f}')
            self.ax.legend(facecolor="#2B2B2B", edgecolor="white", labelcolor="white")
            self._setup_plot_style()

        except Exception as e:
            self.nw_results_box.delete("1.0", "end")
            self.nw_results_box.insert("1.0", f"Erro: {e}")