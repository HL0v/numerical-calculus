# /gui/error_frame.py

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math
from utils.ieee754_converter import get_float_details

class ErrorFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Configure grid weights for the main frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Create main scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self, height=750)
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_rowconfigure(0, weight=1)



        # Move all existing content into scrollable_frame
        # Replace 'self' with 'self.scrollable_frame' in all widget parents

        # --- FLOATING POINT SECTION ---
        fp_frame = ctk.CTkFrame(self.scrollable_frame)
        fp_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        fp_frame.grid_columnconfigure(1, weight=3)
        fp_frame.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(fp_frame, text="1. Aritmética de Ponto Flutuante", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, pady=5, padx=10, sticky="w")
        
        ctk.CTkLabel(fp_frame, text="Número Decimal:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.fp_entry = ctk.CTkEntry(fp_frame, placeholder_text="Ex: 0.1")
        self.fp_entry.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")
        
        fp_button = ctk.CTkButton(fp_frame, text="Analisar", command=self.analyze_float)
        fp_button.grid(row=1, column=2, padx=10, pady=5)
       

        self.fp_results_box = ctk.CTkTextbox(self.scrollable_frame, height=200, state="disabled", font=("Courier", 12))
        self.fp_results_box.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # --- TRUNCATION ERROR SECTION ---
        trunc_frame = ctk.CTkFrame(self.scrollable_frame)
        trunc_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        trunc_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(trunc_frame, text="2. Erro de Aproximação (Truncamento)", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, pady=5, padx=10, sticky="w")
        
        # Inputs Frame
        input_subframe = ctk.CTkFrame(trunc_frame)
        input_subframe.grid(row=1, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
        input_subframe.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(input_subframe, text="Função:").grid(row=0, column=0, padx=10, pady=5)
        self.func_selector = ctk.CTkOptionMenu(input_subframe, values=["sin(x)", "cos(x)", "e^x"])
        self.func_selector.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(input_subframe, text="Valor de x:").grid(row=1, column=0, padx=10, pady=5)
        self.x_entry = ctk.CTkEntry(input_subframe, placeholder_text="Ex: 1.5")
        self.x_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(input_subframe, text="Nº de Termos (n):").grid(row=2, column=0, padx=10, pady=5)
        self.n_entry = ctk.CTkEntry(input_subframe, placeholder_text="Ex: 5")
        self.n_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        trunc_button = ctk.CTkButton(input_subframe, text="Calcular e Plotar", command=self.calculate_truncation)
        trunc_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsw")
        
        self.trunc_results_label = ctk.CTkLabel(input_subframe, text="", justify="left")
        self.trunc_results_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
        
        # Plot Frame
        plot_frame = ctk.CTkFrame(trunc_frame)
        plot_frame.grid(row=2, column=0, padx=10, pady=10, sticky="we", columnspan=2)
        plot_frame.grid_rowconfigure(0, weight=1)
        plot_frame.grid_columnconfigure(0, weight=1)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="we")
        self.setup_plot_style()

    def setup_plot_style(self):
        self.fig.patch.set_facecolor("#2B2B2B")
        self.ax.set_facecolor("#1E1E1E")
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white') 
        self.ax.spines['right'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.title.set_color('white')
        self.canvas.draw()
        
    def analyze_float(self):
        details = get_float_details(self.fp_entry.get())
        if not details:
            result_text = "Entrada inválida. Por favor, insira um número."
        else:
            s32 = details["single"]
            s64 = details["double"]
            
            result_text = (
                f"Entrada: {self.fp_entry.get()}\n"
                f"{'-'*50}\n"
                f"SINGLE PRECISION (32-bit)\n"
                f"{'-'*50}\n"
                f"Sinal: {s32['sign']} | Expoente: {s32['exponent']} | Mantissa: {s32['mantissa']}\n"
                f"Valor Real Armazenado: {s32['reconstructed']:.50f}\n"
                f"Erro de Representação: {float(self.fp_entry.get()) - s32['reconstructed']}\n\n"
                f"{'-'*50}\n"
                f"DOUBLE PRECISION (64-bit)\n"
                f"{'-'*50}\n"
                f"Sinal: {s64['sign']} | Expoente: {s64['exponent']} | Mantissa: {s64['mantissa']}\n"
                f"Valor Real Armazenado: {s64['reconstructed']:.50f}\n"
                f"Erro de Representação: {float(self.fp_entry.get()) - s64['reconstructed']}\n"
            )

        self.fp_results_box.configure(state="normal")
        self.fp_results_box.delete("1.0", "end")
        self.fp_results_box.insert("1.0", result_text)
        self.fp_results_box.configure(state="disabled")

    def calculate_truncation(self):
        try:
            func_name = self.func_selector.get()
            x = float(self.x_entry.get())
            n_terms = int(self.n_entry.get())

            approx_val = 0
            if func_name == "sin(x)":
                true_val = math.sin(x)
                for i in range(n_terms):
                    approx_val += ((-1)**i) * (x**(2*i + 1)) / math.factorial(2*i + 1)
            elif func_name == "cos(x)":
                true_val = math.cos(x)
                for i in range(n_terms):
                    approx_val += ((-1)**i) * (x**(2*i)) / math.factorial(2*i)
            elif func_name == "e^x":
                true_val = math.exp(x)
                for i in range(n_terms):
                    approx_val += (x**i) / math.factorial(i)

            abs_error = abs(true_val - approx_val)
            rel_error = abs(abs_error / true_val) if true_val != 0 else float('inf')

            result_text = (
                f"Valor Verdadeiro: {true_val:.8f}\n"
                f"Valor Aproximado ({n_terms} termos): {approx_val:.8f}\n"
                f"Erro Absoluto: {abs_error:.8f}\n"
                f"Erro Relativo: {rel_error:.8%}"
            )
            self.trunc_results_label.configure(text=result_text)
            
            # Plotting
            self.ax.clear()
            x_range = np.linspace(x - 3, x + 3, 400)
            
            if func_name == "sin(x)":
                y_true = np.sin(x_range)
                y_approx = sum([((-1)**i) * (x_range**(2*i + 1)) / math.factorial(2*i + 1) for i in range(n_terms)])
            elif func_name == "cos(x)":
                y_true = np.cos(x_range)
                y_approx = sum([((-1)**i) * (x_range**(2*i)) / math.factorial(2*i) for i in range(n_terms)])
            elif func_name == "e^x":
                y_true = np.exp(x_range)
                y_approx = sum([(x_range**i) / math.factorial(i) for i in range(n_terms)])

            self.ax.plot(x_range, y_true, label=f"Função Real ({func_name})", color="#007ACC")
            self.ax.plot(x_range, y_approx, label=f"Aproximação ({n_terms} termos)", linestyle='--', color="#FFD700")
            self.ax.axvline(x=x, color='red', linestyle=':', label=f"x = {x}")
            self.ax.legend(facecolor="#2B2B2B", edgecolor="white", labelcolor="white")
            self.ax.set_title(f"Aproximação de {func_name}", color="white")
            self.ax.grid(True, linestyle='--', alpha=0.3)
            self.setup_plot_style()

        except Exception as e:
            self.trunc_results_label.configure(text=f"Erro: {e}")