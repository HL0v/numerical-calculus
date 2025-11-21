import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.interpolate import lagrange

class InterpolationFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Input Area ---
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(input_frame, text="Pontos (x,y):").grid(row=0, column=0, padx=10, pady=5)
        self.points_entry = ctk.CTkEntry(input_frame, placeholder_text="Ex: 1,2; 3,4; 5,1")
        self.points_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Estimar para x =").grid(row=1, column=0, padx=10, pady=5)
        self.estimate_entry = ctk.CTkEntry(input_frame, placeholder_text="Opcional")
        self.estimate_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        calc_btn = ctk.CTkButton(input_frame, text="Calcular Polinómio de Lagrange", command=self.calculate_lagrange)
        calc_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # --- Output Area ---
        self.result_box = ctk.CTkTextbox(self, height=150, font=("Courier", 12))
        self.result_box.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        # --- Plot Area ---
        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.plot_frame.grid_rowconfigure(0, weight=1)
        self.plot_frame.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=2)

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
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.title.set_color('white')
        self.ax.grid(True, linestyle='--', alpha=0.3)
        self.canvas.draw()

    def calculate_lagrange(self):
        try:
            points_str = self.points_entry.get().split(';')
            points = []
            for p in points_str:
                x, y = map(float, p.split(','))
                points.append((x, y))
            
            points.sort() # Sort by x
            X = np.array([p[0] for p in points])
            Y = np.array([p[1] for p in points])

            # Calculate Lagrange Polynomial
            poly = lagrange(X, Y)
            
            # Formatting polynomial string
            coeffs = poly.coef
            degree = len(coeffs) - 1
            poly_str = "Pn(x) = "
            for i, c in enumerate(coeffs):
                power = degree - i
                if abs(c) > 1e-10: # Ignore close to zero
                    sign = "+ " if c >= 0 and i > 0 else "- " if c < 0 else ""
                    poly_str += f"{sign}{abs(c):.4f}*x^{power} "

            result_text = f"Pontos Inseridos: {points}\n\n"
            result_text += f"Polinómio Interpolador (Lagrange):\n{poly_str}\n"

            # Estimate specific value
            est_x_str = self.estimate_entry.get()
            if est_x_str:
                est_x = float(est_x_str)
                est_y = poly(est_x)
                result_text += f"\nEstimativa: P({est_x}) = {est_y:.6f}"

            self.result_box.delete("1.0", "end")
            self.result_box.insert("1.0", result_text)

            # Plotting
            self.ax.clear()
            x_plot = np.linspace(min(X)-1, max(X)+1, 200)
            y_plot = poly(x_plot)
            
            self.ax.plot(x_plot, y_plot, label='Polinómio Pn(x)', color='#007ACC')
            self.ax.scatter(X, Y, color='#FFD700', zorder=5, label='Pontos')
            
            if est_x_str:
                 self.ax.plot(est_x, est_y, 'rx', markersize=10, label=f'Estimativa x={est_x}')

            self.ax.legend(facecolor="#2B2B2B", edgecolor="white", labelcolor="white")
            self.ax.set_title("Interpolação de Lagrange")
            self._setup_plot_style()

        except Exception as e:
            self.result_box.delete("1.0", "end")
            self.result_box.insert("1.0", f"Erro: {e}\nVerifique o formato: x1,y1; x2,y2")