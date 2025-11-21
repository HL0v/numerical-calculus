import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class LeastSquaresFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Settings Frame ---
        settings_frame = ctk.CTkFrame(self)
        settings_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(settings_frame, text="Dados (x,y):").grid(row=0, column=0, padx=5)
        self.data_entry = ctk.CTkEntry(settings_frame, width=300, placeholder_text="Ex: 0,1; 1,2.5; 2,3.8; 3,7")
        self.data_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(settings_frame, text="Método:").grid(row=1, column=0, padx=5)
        self.method_var = ctk.StringVar(value="Linear")
        self.method_menu = ctk.CTkOptionMenu(settings_frame, variable=self.method_var, 
                                             values=["Linear (y=ax+b)", "Polinomial", "Exponencial (y=ae^bx)", "Fourier (Trigonométrico)"],
                                             command=self.update_inputs)
        self.method_menu.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Input extra (grau do polinómio ou n de termos)
        self.extra_param_label = ctk.CTkLabel(settings_frame, text="Grau:")
        self.extra_param_entry = ctk.CTkEntry(settings_frame, width=50)
        # Default hidden/shown based on logic
        
        btn_calc = ctk.CTkButton(settings_frame, text="Ajustar Curva", command=self.calculate_mmq)
        btn_calc.grid(row=2, column=0, columnspan=3, pady=10)

        self.update_inputs("Linear (y=ax+b)")

        # --- Results & Plot ---
        self.results_box = ctk.CTkTextbox(self, height=200, font=("Courier", 12))
        self.results_box.grid(row=1, column=0, padx=10, sticky="ew")
        
        plot_container = ctk.CTkFrame(self)
        plot_container.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        plot_container.grid_rowconfigure(0, weight=1)
        plot_container.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=2)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_container)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        self._setup_plot_style()

    def update_inputs(self, choice):
        if "Polinomial" in choice or "Fourier" in choice:
            self.extra_param_label.grid(row=1, column=2, padx=5)
            self.extra_param_entry.grid(row=1, column=3, padx=5)
            self.extra_param_label.configure(text="Grau/Termos:")
        else:
            self.extra_param_label.grid_forget()
            self.extra_param_entry.grid_forget()

    def _setup_plot_style(self):
        self.fig.patch.set_facecolor("#2B2B2B")
        self.ax.set_facecolor("#242424")
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        for spine in self.ax.spines.values():
            spine.set_edgecolor('white')
        self.ax.grid(True, linestyle='--', alpha=0.3)
        self.canvas.draw()

    def calculate_mmq(self):
        try:
            # Parse Data
            raw_data = self.data_entry.get().split(';')
            X = np.array([float(p.split(',')[0]) for p in raw_data])
            Y = np.array([float(p.split(',')[1]) for p in raw_data])
            
            method = self.method_var.get()
            A = None # Design Matrix
            y_vec = Y
            coeffs = []
            fit_func = None
            model_str = ""
            
            steps_text = f"Dados inseridos: {len(X)} pontos.\n"

            if "Linear" in method:
                # y = ax + b -> y = b + ax (Matriz [1, x])
                A = np.vstack([np.ones(len(X)), X]).T
                steps_text += "Modelo: y = a0 + a1*x\n"
            
            elif "Polinomial" in method:
                degree = int(self.extra_param_entry.get() or 2)
                # y = a0 + a1x + ... + anx^n
                A = np.vander(X, degree + 1, increasing=True)
                steps_text += f"Modelo Polinomial de grau {degree}\n"

            elif "Exponencial" in method:
                # y = a * e^(bx) -> ln(y) = ln(a) + bx
                # Linearizado: Y_lin = A0 + A1*x, onde A0=ln(a), A1=b
                if np.any(Y <= 0):
                    raise ValueError("Para ajuste exponencial, y deve ser > 0.")
                y_vec = np.log(Y)
                A = np.vstack([np.ones(len(X)), X]).T
                steps_text += "Linearização: ln(y) = ln(a) + bx\n"

            elif "Fourier" in method:
                # Aproximação: f(x) = a0 + a1 cos(x) + b1 sin(x) ...
                # Simplificado para período fixo ou assumindo dados em radianos
                terms = int(self.extra_param_entry.get() or 1)
                cols = [np.ones(len(X))]
                for k in range(1, terms + 1):
                    cols.append(np.cos(k * X))
                    cols.append(np.sin(k * X))
                A = np.column_stack(cols)
                steps_text += f"Série de Fourier com {terms} harmónicas\n"

            # Solve Normal Equations: (A^T * A) * c = A^T * y
            At = A.T
            AtA = At @ A
            Aty = At @ y_vec
            
            # Use numpy solve
            coeffs = np.linalg.solve(AtA, Aty)
            
            # Didactic Output
            steps_text += f"\nMatriz de Design A ({A.shape}):\n{np.array2string(A, precision=2)}\n"
            steps_text += f"\nMatriz Normal (A^T * A):\n{np.array2string(AtA, precision=2)}\n"
            steps_text += f"\nVetor (A^T * y):\n{np.array2string(Aty, precision=2)}\n"
            steps_text += f"\nCoeficientes encontrados:\n{coeffs}\n"

            # Construct Plotting Function and Equation String
            x_plot = np.linspace(min(X), max(X), 200)
            y_plot = []

            if "Exponencial" in method:
                a = np.exp(coeffs[0])
                b = coeffs[1]
                model_str = f"y = {a:.4f} * e^({b:.4f}x)"
                y_plot = a * np.exp(b * x_plot)
                # Recalculate error on original scale
                y_est = a * np.exp(b * X)
                total_sq_error = np.sum((Y - y_est)**2)
            
            elif "Fourier" in method:
                y_plot = np.zeros_like(x_plot) + coeffs[0]
                y_est = np.zeros_like(X) + coeffs[0]
                model_str = f"y = {coeffs[0]:.3f}"
                idx = 1
                for k in range(1, int(self.extra_param_entry.get() or 1) + 1):
                    a_k = coeffs[idx]
                    b_k = coeffs[idx+1]
                    term_str = f" + {a_k:.3f}cos({k}x) + {b_k:.3f}sin({k}x)"
                    model_str += term_str
                    y_plot += a_k * np.cos(k * x_plot) + b_k * np.sin(k * x_plot)
                    y_est += a_k * np.cos(k * X) + b_k * np.sin(k * X)
                    idx += 2
                total_sq_error = np.sum((Y - y_est)**2)

            else: # Linear or Polynomial
                # Coeffs are [a0, a1, a2...] (increasing power due to vander logic used)
                # Note: polyval expects decreasing, so we flip for calculation if using polyval,
                # or just dot product
                y_plot = np.dot(np.vander(x_plot, len(coeffs), increasing=True), coeffs)
                y_est = np.dot(A, coeffs)
                total_sq_error = np.sum((Y - y_est)**2)
                
                model_str = "y = " + " + ".join([f"{c:.3f}x^{i}" for i, c in enumerate(coeffs)])

            steps_text += f"\nEquação Final: {model_str}\n"
            steps_text += f"Erro Quadrático Total: {total_sq_error:.6f}"

            self.results_box.delete("1.0", "end")
            self.results_box.insert("1.0", steps_text)

            # Plot
            self.ax.clear()
            self.ax.scatter(X, Y, color='#FFD700', label='Dados Experimentais', s=50, zorder=5)
            self.ax.plot(x_plot, y_plot, color='#007ACC', linewidth=2, label=f'Ajuste ({method.split()[0]})')
            self.ax.legend(facecolor="#2B2B2B", edgecolor="white", labelcolor="white")
            self.ax.set_title(f"Mínimos Quadrados: {method}")
            self._setup_plot_style()

        except Exception as e:
            self.results_box.delete("1.0", "end")
            self.results_box.insert("1.0", f"Erro: {e}\nVerifique os dados.")