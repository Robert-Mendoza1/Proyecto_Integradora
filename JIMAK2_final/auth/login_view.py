import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class LoginView:
    def __init__(self, root):
        self.root = root
        self._on_login = lambda: None
        self._on_open_register = lambda: None
        self._build_ui()

    def _build_ui(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.root.title('Iniciar Sesión - Tienda')
        main_frame = ttk.Frame(self.root, padding=40)
        main_frame.pack(fill='both', expand=True)

        try:
            pil = Image.open('assets/logo.png')
            w,h = pil.size
            new_w = 200
            new_h = int((h / w) * new_w)
            pil = pil.resize((new_w, new_h), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(pil)
            ttk.Label(main_frame, image=self.logo_img).pack(pady=(0,20))
        except Exception:
            ttk.Label(main_frame, text='JIMAK Systems', font=('Arial',18,'bold')).pack(pady=(0,20))

        ttk.Label(main_frame, text='Usuario/Correo').pack(anchor='w')
        self.username_entry = ttk.Entry(main_frame)
        self.username_entry.pack(fill='x', pady=(0,10))
        self.username_entry.focus()

        ttk.Label(main_frame, text='Contraseña').pack(anchor='w')
        self.password_entry = ttk.Entry(main_frame, show='•')
        self.password_entry.pack(fill='x', pady=(0,10))

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=(10,0))
        ttk.Button(btn_frame, text='Entrar', command=lambda: self._on_login()).pack(side='left', expand=True, fill='x', padx=5)
        ttk.Button(btn_frame, text='Registrar', command=lambda: self._on_open_register()).pack(side='left', expand=True, fill='x', padx=5)

        self.root.bind('<Return>', lambda ev: self._on_login())

    def set_login_callback(self, func):
        self._on_login = func

    def set_open_register_callback(self, func):
        self._on_open_register = func

    def get_username(self):
        return self.username_entry.get().strip()

    def get_password(self):
        return self.password_entry.get().strip()
