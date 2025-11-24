# pos_controller.py

def init_state():
    """Retorna el estado inicial del punto de venta."""
    return {
        "cart": [],
        "search_text": ""
    }


# -----------------------------
#       PRODUCTOS
# -----------------------------
def search_products(db, term):
    """Busca productos usando el término ingresado."""
    return db.get_products(term)


def get_product_by_id(db, product_id):
    """Obtiene un producto por ID."""
    for p in db.get_products():
        if p["id"] == product_id:
            return p
    return None


# -----------------------------
#          CARRITO
# -----------------------------
def add_to_cart(state, product, qty=1):
    """Agrega un producto o suma cantidad si ya existe."""
    for item in state["cart"]:
        if item["producto_id"] == product["id"]:
            item["cantidad"] += qty
            item["subtotal"] = item["cantidad"] * product["precio"]
            return

    state["cart"].append({
        "producto_id": product["id"],
        "nombre": product["nombre"],
        "precio": product["precio"],
        "cantidad": qty,
        "subtotal": product["precio"] * qty
    })


def remove_item(state, index):
    """Elimina un producto del carrito."""
    if 0 <= index < len(state["cart"]):
        del state["cart"][index]


def modify_quantity(state, index, new_qty):
    """Modifica cantidad de un producto."""
    item = state["cart"][index]
    item["cantidad"] = new_qty
    item["subtotal"] = new_qty * item["precio"]


def clear_cart(state):
    """Limpia todo el carrito."""
    state["cart"].clear()


def calculate_total(state):
    """Retorna el total del carrito."""
    return sum(item["subtotal"] for item in state["cart"])
