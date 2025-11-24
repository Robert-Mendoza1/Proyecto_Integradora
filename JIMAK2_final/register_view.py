import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

class RegisterView:
    def __init__(self, root):
        self.root = root
        self.entries = {}
        self.role_var = tk.StringVar(value="vendedor")
        self.logo_image = None
        self.setup_ui()

    # ---------------------- UI ----------------------
    def setup_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Registrar Usuario - Tienda")
        self.root.geometry("400x750")
        self.root.configure(bg='white')

        main_frame = ttk.Frame(self.root, padding="40")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self._load_logo(main_frame)

        title_label = ttk.Label(main_frame, text="Registrar Usuario",
                                font=("Arial", 14), foreground="#34495e")
        title_label.pack(pady=(0, 30))

        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.BOTH, expand=True)

        fields = [
            ("Nombre Completo", "nombre"),
            ("Usuario", "username"),
            ("Email", "email"),
            ("Contraseña", "password"),
            ("Confirmar Contraseña", "confirm_password")
        ]

        for i, (label, field) in enumerate(fields):
            ttk.Label(form_frame, text=label, font=("Arial", 10),
                      anchor="center", foreground="#2c3e50").grid(row=i*2, column=0, pady=(10, 5), sticky="ew")

            entry = ttk.Entry(form_frame, width=25, font=("Arial", 10),
                              show="*" if "password" in field else "")
            entry.grid(row=i*2+1, column=0, pady=(0, 10), sticky="ew", ipady=4)
            self.entries[field] = entry

        # Rol selector
        ttk.Label(form_frame, text="Rol", font=("Arial", 9), anchor="center",
                  foreground="#2c3e50").grid(row=len(fields)*2, column=0, pady=(10, 5), sticky="ew")

        role_combo = ttk.Combobox(form_frame, textvariable=self.role_var,
                                  values=["admin", "vendedor"], state="readonly",
                                  width=10, font=("Arial", 10))
        role_combo.grid(row=len(fields)*2+1, column=0, pady=(0, 20), sticky="ew", ipady=4)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 30))

        self.register_button = ttk.Button(button_frame, text="Registrar")
        self.register_button.pack(side=tk.LEFT, padx=(0, 10), expand=True, fill=tk.X)

        self.back_button = ttk.Button(button_frame, text="Volver")
        self.back_button.pack(side=tk.RIGHT, padx=(10, 0), expand=True, fill=tk.X)

        form_frame.grid_columnconfigure(0, weight=1)
        button_frame.pack_propagate(False)
        button_frame.configure(height=40)

        self.center_window()

    def _load_logo(self, parent):
        try:
            pil_image = Image.open("assets/logo.png")
            w, h = pil_image.size
            new_w = 200
            new_h = int((h / w) * new_w)
            resized = pil_image.resize((new_w, new_h), Image.Resampling.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(resized)
            ttk.Label(parent, image=self.logo_image).pack(pady=(0, 20))
        except Exception as e:
            print(f"Error cargando logo: {e}")
            ttk.Label(parent, text="5 JJMAK Systems", font=("Arial", 18, "bold"),
                      foreground="#2c3e50").pack(pady=(0, 30))

    # ---------------------- Helpers ----------------------
    def center_window(self):
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    # ---------------------- Public callbacks ----------------------
    def on_register(self, callback):
        self.register_button.configure(command=callback)

    def on_back(self, callback):
        self.back_button.configure(command=callback)

    def get_form_data(self):
        return {
            field: entry.get().strip()
            for field, entry in self.entries.items()
        }

    def get_role(self):
        return self.role_var.get()

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def show_info(self, message):
        messagebox.showinfo("Éxito", message)