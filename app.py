# /app.py

import customtkinter as ctk
from gui.error_frame import ErrorFrame
from gui.linear_systems_frame import LinearSystemsFrame
from gui.zeros_frames import ZerosFrame
# Importando os novos módulos
from gui.interpolation_frame import InterpolationFrame
from gui.least_squares_frame import LeastSquaresFrame
from gui.integration_frame import IntegrationFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Trabalho de Cálculo Numérico")
        self.geometry("1200x800")

        # --- THEME AND STYLING ---
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # --- CONFIGURE MAIN GRID ---
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- SIDEBAR ---
        self.sidebar_frame = ctk.CTkFrame(self, width=180, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(7, weight=1) # Empurrar o spacer para baixo se necessário

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Módulos", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # --- NAVIGATION BUTTONS ---
        self.sidebar_buttons = {}
        button_info = {
            "errors": "Noções de Erro 🎓",
            "zeros": "Zeros de Funções 🎯",
            "linear": "Sistemas Lineares 🔢",
            "interp": "Interpolação 📈",
            "least_sq": "Mínimos Quadrados 📉",
            "integration": "Integração Numérica ∫"
        }
        
        for i, (name, text) in enumerate(button_info.items()):
            btn = ctk.CTkButton(self.sidebar_frame, text=text, command=lambda n=name: self.select_frame_by_name(n))
            btn.grid(row=i+1, column=0, padx=20, pady=10)
            self.sidebar_buttons[name] = btn

        # --- CONTENT FRAMES ---
        self.frames = {}
        # Create an instance of each frame
        self.frames["errors"] = ErrorFrame(self)
        self.frames["zeros"] = ZerosFrame(self)
        self.frames["linear"] = LinearSystemsFrame(self)
        self.frames["interp"] = InterpolationFrame(self)
        self.frames["least_sq"] = LeastSquaresFrame(self)
        self.frames["integration"] = IntegrationFrame(self)

        # --- SET INITIAL FRAME ---
        self.select_frame_by_name("errors")
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def select_frame_by_name(self, name):
        # Reset button styles
        for btn_name, btn in self.sidebar_buttons.items():
            btn.configure(fg_color=("gray75", "gray25")) # Default color

        # Highlight the selected button
        self.sidebar_buttons[name].configure(fg_color=("#1f538d")) # Highlight color

        # Hide all other frames
        for frame_name, frame in self.frames.items():
            if frame.winfo_ismapped():
                frame.grid_forget()

        # Show the selected frame
        selected_frame = self.frames[name]
        selected_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    def on_closing(self):
        self.quit()

if __name__ == "__main__":
    app = App()
    app.mainloop()