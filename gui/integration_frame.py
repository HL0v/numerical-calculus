import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sympy
from matplotlib.patches import Polygon

class IntegrationFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.tab_view = ctk.CTkTabview(self, anchor="w")
        self.tab_view.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.tab_view.add("Newton-Cotes")
        self.tab_view.add("Quadratura de Gauss")

        self._create_newton_cotes_tab(self.tab_view.tab("Newton-Cotes"))
        self._create_gauss_tab(self.tab_view.tab("Quadratura de Gauss"))

        # Plot area shared or recreated per tab? Let's put it below the tabs
        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.plot_frame.grid_rowconfigure(0, weight=1)
        self.plot_frame.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        self._setup_plot_style()

    def _setup_plot_style(self):
        self.fig.patch.set_facecolor("#2B2B2B")
        self.ax.set_facecolor("#242424")
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        for spine in self.ax.spines.values():
            spine.set_edgecolor('white')
        self.ax.grid(True, linestyle='--', alpha=0.3)
        self.canvas.draw()

    def _safe_eval(self, func_str):
        x = sympy.symbols('x')
        try:
            expr = sympy.sympify(func_str, locals={'e': sympy.E, 'pi': sympy.pi, 'sin': sympy.sin, 'cos': sympy.cos, 'exp': sympy.exp, 'log': sympy.log})
            f_lamb = sympy.lambdify(x, expr, 'numpy')
            return f_lamb, expr
        except:
            return None, None

    # --- NEWTON-COTES ---
    def _create_newton_cotes_tab(self, tab):
        tab.grid_columnconfigure(1, weight=1)
        
        input_frame = ctk.CTkFrame(tab)
        input_frame.grid(row=0, column=0, sticky="ns", padx=5, pady=5)
        
        ctk.CTkLabel(input_frame, text="Função f(x):").pack(pady=2)
        self.nc_func = ctk.CTkEntry(input_frame, placeholder_text="Ex: x**2 + 1")
        self.nc_func.pack(pady=2)

        ctk.CTkLabel(input_frame, text="Intervalo [a, b]:").pack(pady=2)
        frame_ab = ctk.CTkFrame(input_frame, fg_color="transparent")
        frame_ab.pack()
        self.nc_a = ctk.CTkEntry(frame_ab, width=50, placeholder_text="a")
        self.nc_a.pack(side="left", padx=2)
        self.nc_b = ctk.CTkEntry(frame_ab, width=50, placeholder_text="b")
        self.nc_b.pack(side="left", padx=2)

        ctk.CTkLabel(input_frame, text="Subintervalos (N):").pack(pady=2)
        self.nc_n = ctk.CTkEntry(input_frame, placeholder_text="Inteiro")
        self.nc_n.pack(pady=2)

        ctk.CTkLabel(input_frame, text="Regra:").pack(pady=2)
        self.nc_method = ctk.CTkOptionMenu(input_frame, values=["Trapézio", "Simpson 1/3", "Simpson 3/8"])
        self.nc_method.pack(pady=2)

        ctk.CTkButton(input_frame, text="Calcular", command=self.calc_newton_cotes).pack(pady=10)

        self.nc_result = ctk.CTkTextbox(tab, font=("Courier", 12))
        self.nc_result.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    def calc_newton_cotes(self):
        try:
            f, expr = self._safe_eval(self.nc_func.get())
            a = float(self.nc_a.get())
            b = float(self.nc_b.get())
            N = int(self.nc_n.get())
            method = self.nc_method.get()

            if f is None: raise ValueError("Função inválida")

            # Exact integral for comparison
            x_sym = sympy.symbols('x')
            exact_val = float(sympy.integrate(expr, (x_sym, a, b)))
            
            h = (b - a) / N
            x_vals = np.linspace(a, b, N + 1)
            y_vals = f(x_vals)
            
            result = 0
            formula_str = ""

            if method == "Trapézio":
                result = (h/2) * (y_vals[0] + 2*np.sum(y_vals[1:-1]) + y_vals[-1])
                formula_str = "I ≈ (h/2) * [f(x0) + 2∑f(xi) + f(xn)]"
            
            elif method == "Simpson 1/3":
                if N % 2 != 0: raise ValueError("Para Simpson 1/3, N deve ser par.")
                result = (h/3) * (y_vals[0] + 4*np.sum(y_vals[1:-1:2]) + 2*np.sum(y_vals[2:-1:2]) + y_vals[-1])
                formula_str = "I ≈ (h/3) * [f(x0) + 4∑ímpar + 2∑par + f(xn)]"

            elif method == "Simpson 3/8":
                if N % 3 != 0: raise ValueError("Para Simpson 3/8, N deve ser múltiplo de 3.")
                result = (3*h/8) * (y_vals[0] + 3*np.sum(y_vals[1:-1]) - np.sum(y_vals[3:-1:3]) + y_vals[-1]) # Simplified logic needed but standard formula used
                # Standard generic loop is safer for 3/8
                s = y_vals[0] + y_vals[-1]
                for i in range(1, N):
                    if i % 3 == 0: s += 2 * y_vals[i]
                    else: s += 3 * y_vals[i]
                result = (3 * h / 8) * s
                formula_str = "I ≈ (3h/8) * [f(x0) + 3*f(x1) + 3*f(x2) + 2*f(x3) + ...]"

            error = abs(exact_val - result)
            
            out = f"Método: {method} (N={N})\n"
            out += f"Passo h = {h:.6f}\n"
            out += f"Fórmula: {formula_str}\n"
            out += "-"*40 + "\n"
            out += f"Valor Calculado: {result:.8f}\n"
            out += f"Valor Exato:     {exact_val:.8f}\n"
            out += f"Erro Absoluto:   {error:.8e}\n"

            self.nc_result.delete("1.0", "end")
            self.nc_result.insert("1.0", out)
            
            # Visualizing
            self.ax.clear()
            x_plot = np.linspace(a - 0.5, b + 0.5, 200)
            self.ax.plot(x_plot, f(x_plot), color="#007ACC", label="f(x)")
            self.ax.fill_between(x_vals, y_vals, alpha=0.3, color="#FFD700", label="Área Aproximada")
            self.ax.scatter(x_vals, y_vals, color="red", s=10)
            self.ax.set_title(f"Integração Numérica - {method}")
            self.ax.legend(facecolor="#2B2B2B", edgecolor="white", labelcolor="white")
            self._setup_plot_style()

        except Exception as e:
            self.nc_result.delete("1.0", "end")
            self.nc_result.insert("1.0", f"Erro: {e}")

    # --- GAUSS QUADRATURE ---
    def _create_gauss_tab(self, tab):
        tab.grid_columnconfigure(1, weight=1)
        
        input_frame = ctk.CTkFrame(tab)
        input_frame.grid(row=0, column=0, sticky="ns", padx=5, pady=5)
        
        ctk.CTkLabel(input_frame, text="Função f(x):").pack(pady=2)
        self.gq_func = ctk.CTkEntry(input_frame, placeholder_text="Ex: exp(x)")
        self.gq_func.pack(pady=2)

        ctk.CTkLabel(input_frame, text="Intervalo [a, b]:").pack(pady=2)
        frame_ab = ctk.CTkFrame(input_frame, fg_color="transparent")
        frame_ab.pack()
        self.gq_a = ctk.CTkEntry(frame_ab, width=50, placeholder_text="a")
        self.gq_a.pack(side="left", padx=2)
        self.gq_b = ctk.CTkEntry(frame_ab, width=50, placeholder_text="b")
        self.gq_b.pack(side="left", padx=2)

        ctk.CTkLabel(input_frame, text="Pontos de Gauss (n):").pack(pady=2)
        self.gq_n = ctk.CTkOptionMenu(input_frame, values=["2", "3", "4"])
        self.gq_n.pack(pady=2)

        ctk.CTkButton(input_frame, text="Calcular", command=self.calc_gauss).pack(pady=10)

        self.gq_result = ctk.CTkTextbox(tab, font=("Courier", 12))
        self.gq_result.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    def calc_gauss(self):
        try:
            f, expr = self._safe_eval(self.gq_func.get())
            a = float(self.gq_a.get())
            b = float(self.gq_b.get())
            n = int(self.gq_n.get())

            if f is None: raise ValueError("Função inválida")

            # Weights and Roots for [-1, 1]
            if n == 2:
                t = np.array([-1/np.sqrt(3), 1/np.sqrt(3)])
                w = np.array([1, 1])
            elif n == 3:
                t = np.array([-np.sqrt(3/5), 0, np.sqrt(3/5)])
                w = np.array([5/9, 8/9, 5/9])
            elif n == 4:
                t = np.array([-np.sqrt(3/7 + 2/7*np.sqrt(6/5)), -np.sqrt(3/7 - 2/7*np.sqrt(6/5)),
                              np.sqrt(3/7 - 2/7*np.sqrt(6/5)), np.sqrt(3/7 + 2/7*np.sqrt(6/5))])
                w = np.array([(18-np.sqrt(30))/36, (18+np.sqrt(30))/36,
                              (18+np.sqrt(30))/36, (18-np.sqrt(30))/36])

            # Change of variables
            # x = ((b-a)*t + (b+a))/2
            # dx = ((b-a)/2) dt
            
            x_mapped = ((b - a) * t + (b + a)) / 2
            factor = (b - a) / 2
            
            result = factor * np.sum(w * f(x_mapped))

            # Verification
            x_sym = sympy.symbols('x')
            exact_val = float(sympy.integrate(expr, (x_sym, a, b)))
            error = abs(exact_val - result)

            out = f"Quadratura de Gauss (n={n} pontos)\n"
            out += f"Mudança de variável: [-1, 1] -> [{a}, {b}]\n"
            out += "-"*40 + "\n"
            out += "Pontos t_i (Normaliz) | Pesos w_i | x_i (Mapeado) | f(x_i)\n"
            for i in range(n):
                out += f"{t[i]:.6f}          | {w[i]:.6f}  | {x_mapped[i]:.6f}    | {f(x_mapped[i]):.6f}\n"
            
            out += "-"*40 + "\n"
            out += f"Integral Calculado: {result:.8f}\n"
            out += f"Integral Exato:     {exact_val:.8f}\n"
            out += f"Erro:               {error:.8e}"

            self.gq_result.delete("1.0", "end")
            self.gq_result.insert("1.0", out)

            # Plot
            self.ax.clear()
            x_plot = np.linspace(a - 0.5, b + 0.5, 200)
            self.ax.plot(x_plot, f(x_plot), color="#007ACC", label="f(x)")
            # Show rectangles for Gauss points (conceptual)
            for i in range(n):
                self.ax.plot([x_mapped[i], x_mapped[i]], [0, f(x_mapped[i])], 'r--', alpha=0.5)
                self.ax.plot(x_mapped[i], f(x_mapped[i]), 'ro')
            
            self.ax.fill_between(x_plot, 0, f(x_plot), where=(x_plot>=a) & (x_plot<=b), color="#FFD700", alpha=0.2, label="Área")
            self.ax.set_title(f"Quadratura de Gauss (n={n})")
            self.ax.legend(facecolor="#2B2B2B", edgecolor="white", labelcolor="white")
            self._setup_plot_style()

        except Exception as e:
            self.gq_result.delete("1.0", "end")
            self.gq_result.insert("1.0", f"Erro: {e}")