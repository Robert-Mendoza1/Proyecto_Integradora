import tkinter as tk
from tkinter import ttk, messagebox

class ProveedoresView:
    def __init__(self, parent, db):
        self.db = db
        self.window = tk.Toplevel(parent)
        self.window.title('Proveedores')
        self.window.geometry('650x450')
        self.setup_ui()

    def setup_ui(self):
        top = ttk.Frame(self.window, padding=10); top.pack(fill='x')
        ttk.Label(top, text='Buscar (nombre o teléfono):').pack(side='left')
        self.search_var = tk.StringVar(); self.search_entry = ttk.Entry(top, textvariable=self.search_var, width=40); self.search_entry.pack(side='left', padx=(5,10))
        ttk.Button(top, text='Buscar', command=lambda: None).pack(side='left')
        mid = ttk.Frame(self.window, padding=10); mid.pack(fill='both', expand=True)
        columns = ('id','nombre','telefono','empresa')
        self.tree = ttk.Treeview(mid, columns=columns, show='headings')
        for col in columns: self.tree.heading(col, text=col.capitalize())
        self.tree.column('id', width=40, anchor='center'); self.tree.pack(fill='both', expand=True, side='left')
        scrollbar = ttk.Scrollbar(mid, orient='vertical', command=self.tree.yview); self.tree.configure(yscrollcommand=scrollbar.set); scrollbar.pack(side='left', fill='y')
        bottom = ttk.Frame(self.window, padding=10); bottom.pack(fill='x')
        ttk.Button(bottom, text='Agregar proveedor', command=lambda: None).pack(side='left')
        ttk.Button(bottom, text='Cerrar', command=self.window.destroy).pack(side='right')
    def set_search_callback(self, func): self.search_cb = func; self.window.bind('<Return>', lambda e: self.search_cb())
    def set_add_callback(self, func): self.add_cb = func
    def get_search_text(self): return self.search_var.get().strip()
    def populate(self, rows):
        for i in self.tree.get_children(): self.tree.delete(i)
        for r in rows: self.tree.insert('', 'end', values=(r.get('idProveedor', r.get('id')), r['nombre'], r['telefono'], r.get('empresa','')))
    def show_message(self, msg): messagebox.showinfo('Info', msg)
    def show_error(self, msg): messagebox.showerror('Error', msg)
