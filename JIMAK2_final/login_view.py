import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class LoginView:
    def __init__(self, root):
        self.root = root
        self.username_entry = None
        self.password_entry = None
        self.logo_image = None

    def build_ui(self, on_login, on_open_register):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Iniciar Sesión - Tienda")
        self.root.geometry("400x500")
        self.root.configure(bg='white')

        main_frame = ttk.Frame(self.root, padding="40")
        main_frame.pack(fill=tk.BOTH, expand=True)

        try:
            pil_image = Image.open("assets/logo.png")
            original_width, original_height = pil_image.size
            new_width = 200
            new_height = int((original_height / original_width) * new_width)
            resized_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(resized_image)
            logo_label = ttk.Label(main_frame, image=self.logo_image)
            logo_label.pack(pady=(0, 20))
        except Exception:
            logo_label = ttk.Label(
                main_frame,
                text="5 JJMAK Systems",
                font=("Arial", 18, "bold"),
                foreground="#2c3e50"
            )
            logo_label.pack(pady=(0, 30))

        title_label = ttk.Label(
            main_frame,
            text="Inicio de sesión",
            font=("Arial", 14),
            foreground="#34495e"
        )
        title_label.pack(pady=(0, 30))

        ttk.Label(
            main_frame,
            text="Usuario/Correo",
            font=("Arial", 10),
            width=100,
            anchor="center",
            foreground="#2c3e50"
        ).pack(anchor=tk.W, pady=(0, 5))

        self.username_entry = ttk.Entry(main_frame, width=20, font=("Arial", 16))
        self.username_entry.pack(fill=tk.X, pady=(0, 20))
        self.username_entry.focus()

        ttk.Label(
            main_frame,
            text="Contraseña",
            font=("Arial", 10),
            width=100,
            anchor="center",
            foreground="#2c3e50"
        ).pack(anchor=tk.W, pady=(0, 5))

        self.password_entry = ttk.Entry(main_frame, width=20, show="•", font=("Arial", 16))
        self.password_entry.pack(fill=tk.X, pady=(0, 30))

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 30))

        ttk.Button(
            button_frame,
            text="Entrar",
            command=on_login,
            style="White.TButton"
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        ttk.Button(
            button_frame,
            text="Registrar",
            command=on_open_register,
            style="White.TButton"
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        style = ttk.Style()
        style.configure(
            "White.TButton",
            background="white",
            foreground="black",
            bordercolor="black",
            borderwidth=1,
            relief="solid",
            font=("Arial", 11)
        )
        style.map(
            "White.TButton",
            background=[('active', '#eeeeee'), ('pressed', 'lightgray')],
            foreground=[('active', 'black')]
        )

        self.root.bind('<Return>', lambda event: on_login())
        main_frame.focus_set()

    def get_credentials(self):
        return self.username_entry.get().strip(), self.password_entry.get()
