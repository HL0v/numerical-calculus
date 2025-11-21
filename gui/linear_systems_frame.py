import customtkinter as ctk
import numpy as np
from scipy.linalg import hilbert

class LinearSystemsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.tab_view = ctk.CTkTabview(self, anchor="w")
        self.tab_view.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.tab_view.add("Eliminação de Gauss")

        self.matrix_entries = []
        
        self._create_gauss_tab(self.tab_view.tab("Eliminação de Gauss"))

    def _create_matrix_grid(self, parent, size, grid_row, grid_col, has_b=True, has_x0=False):
        """Dynamically creates a grid of CTkEntry widgets for a matrix."""
        # Clear previous grid if it exists
        if hasattr(self, f'{parent}_grid_frame'):
            getattr(self, f'{parent}_grid_frame').destroy()

        grid_frame = ctk.CTkFrame(parent)
        grid_frame.grid(row=grid_row, column=grid_col, columnspan=5, pady=10, padx=10, sticky="ns")
        setattr(self, f'{parent}_grid_frame', grid_frame)

        entries = {'A': [], 'b': [], 'x0': []}
        
        # Matrix A
        for r in range(size):
            row_entries = []
            for c in range(size):
                entry = ctk.CTkEntry(grid_frame, width=50, justify='center')
                entry.grid(row=r, column=c, padx=2, pady=2)
                row_entries.append(entry)
            entries['A'].append(row_entries)
        
        # Vector b
        if has_b:
            ctk.CTkLabel(grid_frame, text="|").grid(row=0, column=size, rowspan=size)
            b_entries = []
            for r in range(size):
                entry = ctk.CTkEntry(grid_frame, width=50, justify='center')
                entry.grid(row=r, column=size + 1, padx=2, pady=2)
                b_entries.append(entry)
            entries['b'] = b_entries

        # Vector x0
        if has_x0:
            ctk.CTkLabel(grid_frame, text="x₀:").grid(row=size, column=0, pady=(10,0))
            x0_entries = []
            for c in range(size):
                entry = ctk.CTkEntry(grid_frame, width=50, justify='center')
                entry.grid(row=size, column=c+1, padx=2, pady=2)
                x0_entries.append(entry)
            entries['x0'] = x0_entries
            
        return entries

    def _read_matrix_grid(self, entries, size):
        try:
            A = np.zeros((size, size))
            b = np.zeros(size)
            x0 = np.zeros(size)
            
            for r in range(size):
                for c in range(size):
                    A[r, c] = float(entries['A'][r][c].get())
            
            if entries['b']:
                for r in range(size):
                    b[r] = float(entries['b'][r].get())
            
            if entries['x0']:
                for r in range(size):
                    x0[r] = float(entries['x0'][r].get())
                    
            return A, b, x0
        except (ValueError, IndexError):
            return None, None, None

    # --- GAUSSIAN ELIMINATION TAB ---
    def _create_gauss_tab(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        
        controls_frame = ctk.CTkFrame(tab)
        controls_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(controls_frame, text="Tamanho da Matriz:").grid(row=0, column=0, padx=10)
        self.gauss_size_var = ctk.IntVar(value=3)
        size_menu = ctk.CTkOptionMenu(controls_frame, values=["2", "3", "4", "5"], 
                                      variable=self.gauss_size_var, command=self.update_gauss_grid)
        size_menu.grid(row=0, column=1, padx=10)
        
        self.gauss_pivot_var = ctk.BooleanVar(value=True)
        pivot_check = ctk.CTkCheckBox(controls_frame, text="Usar Pivotamento Parcial", variable=self.gauss_pivot_var)
        pivot_check.grid(row=0, column=2, padx=10)

        solve_button = ctk.CTkButton(controls_frame, text="Resolver Sistema", command=self.solve_gauss)
        solve_button.grid(row=0, column=3, padx=20)
        
        self.gauss_results_box = ctk.CTkTextbox(tab, font=("Courier", 12))
        self.gauss_results_box.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        tab.grid_rowconfigure(2, weight=1)
        
        self.update_gauss_grid(3) # Initial grid

    def update_gauss_grid(self, size_str):
        size = int(size_str)
        self.gauss_entries = self._create_matrix_grid(self.tab_view.tab("Eliminação de Gauss"), size, grid_row=1, grid_col=0)

    def solve_gauss(self):
        size = self.gauss_size_var.get()
        A, b, _ = self._read_matrix_grid(self.gauss_entries, size)
        
        if A is None:
            self.gauss_results_box.delete("1.0", "end")
            self.gauss_results_box.insert("1.0", "Erro: Entrada inválida. Verifique os números da matriz.")
            return

        use_pivoting = self.gauss_pivot_var.get()
        n = len(b)
        M = np.hstack([A, b.reshape(-1, 1)])
        
        steps = f"Matriz Aumentada Inicial:\n{M}\n\n"

        # Forward Elimination
        for k in range(n - 1):
            if use_pivoting:
                # Find max in column k and swap
                max_row = k + np.argmax(np.abs(M[k:, k]))
                if max_row != k:
                    M[[k, max_row]] = M[[max_row, k]]
                    steps += f"--- Pivotamento: Troca L{k+1} <-> L{max_row+1} ---\n{M}\n\n"
            
            for i in range(k + 1, n):
                factor = M[i, k] / M[k, k]
                M[i, k:] = M[i, k:] - factor * M[k, k:]
                steps += f"--- L{i+1} = L{i+1} - ({factor:.3f})*L{k+1} ---\n{M}\n\n"
        
        steps += "--- Fim da Eliminação ---\n"
        
        # Back Substitution
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            x[i] = (M[i, -1] - np.dot(M[i, i+1:n], x[i+1:n])) / M[i, i]
        
        steps += f"\nSolução (Vetor x):\n{x}\n"
        
        self.gauss_results_box.delete("1.0", "end")
        self.gauss_results_box.insert("1.0", steps)