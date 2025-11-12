from db import conectar

def buscar_producto_por_codigo(codigo):
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id, nombre, precio, stock FROM productos WHERE codigo_barras = %s", (codigo,))
    producto = cur.fetchone()
    con.close()
    return producto

def actualizar_stock(id_producto, nuevo_stock):
    con = conectar()
    cur = con.cursor()
    cur.execute("UPDATE productos SET stock = %s WHERE id = %s", (nuevo_stock, id_producto))
    con.commit()
    con.close()

def listar_productos():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id, nombre, precio, stock FROM productos")
    productos = cur.fetchall()
    print("\n--- INVENTARIO ---")
    for p in productos:
        print(f"ID: {p[0]} | {p[1]} | ${p[2]} | Stock: {p[3]}")
    con.close()
    input("\nPresione Enter para continuar...")

def agregar_producto():
    codigo_barras = input("Código de barras: ")
    nombre = input("Nombre del producto: ")
    precio = float(input("Precio: "))
    stock = int(input("Stock inicial: "))

    con = conectar()
    cur = con.cursor()
    cur.execute("INSERT INTO productos (codigo_barras, nombre, precio, stock) VALUES (%s, %s, %s, %s)",
                (codigo_barras, nombre, precio, stock))
    con.commit()
    con.close()
    print("Producto agregado correctamente.")
    input("Presione Enter para continuar...")

def editar_producto():
    from helpers import limpiar_pantalla
    codigo = input("Ingrese el código de barras del producto a editar: ")
    producto = buscar_producto_por_codigo(codigo)

    if not producto:
        print("Producto no encontrado.")
        input("Presione Enter para continuar...")
        return

    id_prod, nombre, precio, stock = producto
    limpiar_pantalla()
    print(f"\nProducto encontrado: {nombre} (${precio}) | Stock: {stock}")

    print("\n--- Campos editables ---")
    print("1. Nombre")
    print("2. Precio")
    print("3. Stock")
    print("4. Cancelar")
    opcion = input("Seleccione el campo a editar: ")

    con = conectar()
    cur = con.cursor()

    if opcion == "1":
        nuevo_nombre = input("Nuevo nombre: ")
        cur.execute("UPDATE productos SET nombre = %s WHERE id = %s", (nuevo_nombre, id_prod))
        print("Nombre actualizado.")
    elif opcion == "2":
        nuevo_precio = float(input("Nuevo precio: "))
        cur.execute("UPDATE productos SET precio = %s WHERE id = %s", (nuevo_precio, id_prod))
        print("Precio actualizado.")
    elif opcion == "3":
        nuevo_stock = int(input("Nuevo stock: "))
        cur.execute("UPDATE productos SET stock = %s WHERE id = %s", (nuevo_stock, id_prod))
        print("Stock actualizado.")
    elif opcion == "4":
        print("Edición cancelada.")
        con.close()
        return
    else:
        print("Opción no válida.")
        con.close()
        return

    con.commit()
    con.close()
    input("Presione Enter para continuar...")
