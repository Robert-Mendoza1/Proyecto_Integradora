import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class RegisterView:
    def __init__(self, root):
        self.root = root
        self.entries = {}
        self.role_var = tk.StringVar(value='vendedor')
        self._on_save = lambda: None
        self.build_ui()

    def build_ui(self):
        for w in self.root.winfo_children(): w.destroy()
        main_frame = ttk.Frame(self.root, padding=40)
        main_frame.pack(fill='both', expand=True)

        try:
            pil = Image.open('assets/logo.png')
            pil = pil.resize((200, int(200 * pil.size[1]/pil.size[0])), Image.Resampling.LANCZOS)
            self.logo = ImageTk.PhotoImage(pil)
            ttk.Label(main_frame, image=self.logo).pack(pady=(0,20))
        except:
            ttk.Label(main_frame, text='JIMAK Systems', font=('Arial',18,'bold')).pack(pady=(0,20))

        fields = [('Nombre Completo','nombre'),('Usuario','username'),('Email','email'),
                  ('Contraseña','password'),('Confirmar Contraseña','confirm_password')]
        for label, field in fields:
            ttk.Label(main_frame, text=label).pack(anchor='w')
            e = ttk.Entry(main_frame, show='*' if 'password' in field else '')
            e.pack(fill='x', pady=(0,8))
            self.entries[field]=e

        ttk.Label(main_frame, text='Rol').pack(anchor='w')
        role_combo = ttk.Combobox(main_frame, values=['admin','vendedor'], textvariable=self.role_var, state='readonly')
        role_combo.pack(fill='x', pady=(0,10))

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=(10,0))
        ttk.Button(btn_frame, text='Registrar', command=lambda: self._on_save()).pack(side='left', expand=True, fill='x', padx=5)
        ttk.Button(btn_frame, text='Volver', command=self.back_to_login).pack(side='left', expand=True, fill='x', padx=5)

    def set_save_callback(self, func):
        self._on_save = func

    def get_form_data(self):
        return {k: v.get().strip() for k,v in self.entries.items()}

    def get_role(self):
        return self.role_var.get()

    def show_success(self, msg):
        messagebox.showinfo('Éxito', msg)

    def show_error(self, msg):
        messagebox.showerror('Error', msg)

    def back_to_login(self):
        from auth.login_view import LoginView
        from auth.login_controller import LoginController
        lv = LoginView(self.root)
        LoginController(lv, None)
