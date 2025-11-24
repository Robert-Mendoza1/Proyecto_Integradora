# pos_view.py

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from punto_venta_controller import *
from datetime import datetime


class PointOfSaleWindow:
    def __init__(self, root, user, db):
        self.root = root
        self.user = user
        self.db = db

        # Estado general manejado por el controller
        self.state = init_state()

        self.setup_ui()


    # ------------------------------------------------------
    #                    INTERFAZ
    # ------------------------------------------------------
    def setup_ui(self):
        for w in self.root.winfo_children():
            w.destroy()

        self.root.title("Punto de Venta")
        self.root.geometry("1000x700")

        # Entrada de búsqueda
        self.search_var = tk.StringVar()
        entry = ttk.Entry(self.root, textvariable=self.search_var)
        entry.pack(fill=tk.X, padx=10, pady=10)
        entry.bind("<KeyRelease>", self.update_product_list)

        # Tabla de productos
        self.results_tree = ttk.Treeview(
            self.root,
            columns=("codigo", "nombre", "precio", "stock"),
            show="headings"
        )
        for col in ("codigo", "nombre", "precio", "stock"):
            self.results_tree.heading(col, text=col)
        self.results_tree.pack(fill=tk.BOTH, expand=True, padx=10)
        self.results_tree.bind("<Double-1>", self.on_product_double_click)

        # Tabla del carrito
        self.cart_tree = ttk.Treeview(
            self.root,
            columns=("nombre", "cantidad", "precio", "subtotal"),
            show="headings"
        )
        for col in ("nombre", "cantidad", "precio", "subtotal"):
            self.cart_tree.heading(col, text=col)
        self.cart_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Total
        self.total_label = ttk.Label(self.root, text="Total: $0.00", font=("Arial", 14))
        self.total_label.pack()

        # Botones
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Confirmar Compra", command=self.confirm_purchase).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpiar Carrito", command=self.clear_cart_view).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cerrar Sesión", command=self.logout).pack(side=tk.LEFT, padx=5)

        # Cargar productos
        self.update_product_list()


    # ------------------------------------------------------
    #           EVENTOS DE LA INTERFAZ (View)
    # ------------------------------------------------------
    def update_product_list(self, event=None):
        term = self.search_var.get()
        products = search_products(self.db, term)

        for i in self.results_tree.get_children():
            self.results_tree.delete(i)

        for p in products:
            self.results_tree.insert(
                "",
                "end",
                values=(p["codigo_barras"], p["nombre"], p["precio"], p["stock"]),
                tags=(p["id"],)
            )

    def on_product_double_click(self, event):
        selection = self.results_tree.selection()
        if not selection:
            return

        row = self.results_tree.item(selection[0])
        product_id = row["tags"][0]
        product = get_product_by_id(self.db, product_id)

        qty = simpledialog.askinteger("Cantidad", f"¿Cuántas unidades de {product['nombre']}?")
        if qty and qty > 0:
            add_to_cart(self.state, product, qty)
            self.refresh_cart()

    def refresh_cart(self):
        for i in self.cart_tree.get_children():
            self.cart_tree.delete(i)

        for idx, item in enumerate(self.state["cart"]):
            self.cart_tree.insert(
                "",
                "end",
                values=(item["nombre"], item["cantidad"], item["precio"], item["subtotal"]),
                tags=(idx,)
            )

        total = calculate_total(self.state)
        self.total_label.config(text=f"Total: ${total:.2f}")

    def clear_cart_view(self):
        if messagebox.askyesno("Confirmar", "¿Desea limpiar el carrito?"):
            clear_cart(self.state)
            self.refresh_cart()

    def confirm_purchase(self):
        if not self.state["cart"]:
            messagebox.showwarning("Advertencia", "El carrito está vacío")
            return

        total = calculate_total(self.state)
        messagebox.showinfo("Compra Realizada", f"Total: ${total:.2f}")

        clear_cart(self.state)
        self.refresh_cart()

    def logout(self):
        from login import LoginWindow
        LoginWindow(self.root)
