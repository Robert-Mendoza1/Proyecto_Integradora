import os
from datetime import datetime
from db import conectar
from productos import buscar_producto_por_codigo, actualizar_stock
from helpers import limpiar_pantalla
from decimal import Decimal



# ============================
# 🔹 Registrar venta
# ============================
def registrar_venta(total):
    con = conectar()
    cur = con.cursor()
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cur.execute("INSERT INTO ventas (fecha, total) VALUES (%s, %s)", (fecha, total))
    con.commit()
    id_venta = cur.lastrowid
    con.close()
    return id_venta


def registrar_venta_detalle(id_venta, id_producto, cantidad, subtotal):
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO detalle_venta (venta_id, producto_id, cantidad, subtotal) VALUES (%s, %s, %s, %s)",
        (id_venta, id_producto, cantidad, subtotal)
    )
    con.commit()
    con.close()


# ============================
# 🔹 Ver ventas del día
# ============================
def registrar_ventas_del_dia():
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        SELECT v.id, v.fecha, v.total
        FROM ventas v
        WHERE DATE(v.fecha) = CURDATE()
        ORDER BY v.fecha DESC
    """)
    ventas = cur.fetchall()
    limpiar_pantalla()
    print("\n=== 🧾 VENTAS DEL DÍA ===")

    if not ventas:
        print("No hay ventas registradas hoy.")
        con.close()
        input("\nPresione Enter para continuar...")
        return

    for venta in ventas:
        id_venta, fecha, total = venta
        print(f"\n🕒 Venta ID: {id_venta} | Fecha: {fecha} | Total: ${total:.2f}")

        # Mostrar productos
        cur.execute("""
            SELECT p.nombre, d.cantidad, d.subtotal
            FROM detalle_venta d
            JOIN productos p ON d.producto_id = p.id
            WHERE d.venta_id = %s
        """, (id_venta,))
        detalles = cur.fetchall()

        for det in detalles:
            nombre, cantidad, subtotal = det
            print(f"  - {cantidad} x {nombre} = ${subtotal:.2f}")

    con.close()
    input("\nPresione Enter para continuar...")


# ============================
# 🔹 Menú de opciones
# ============================
def menu_opciones():
    from productos import listar_productos, agregar_producto, editar_producto
    while True:
        limpiar_pantalla()
        print("\n--- MENÚ DE OPCIONES ---")
        print("1. Ver inventario")
        print("2. Agregar producto")
        print("3. Editar producto")
        print("4. Volver")
        opcion = input("Opción: ")

        if opcion == "1":
            listar_productos()
        elif opcion == "2":
            agregar_producto()
        elif opcion == "3":
            editar_producto()
        elif opcion == "4":
            break
        else:
            print("Opción no válida.")
            input("Presione Enter para continuar...")


# ============================
# 🔹 Terminal de venta (loop)
# ============================
def terminal_venta():
    while True:  # 🔁 Permitir múltiples ventas seguidas
        venta = []
        total = Decimal('0.00')

        while True:  # 🔁 Escanear productos
            print("\n=== NUEVA VENTA ===")
            print(" Escanear producto")
            print("1. Mostrar total actual")
            print("2. Finalizar venta y cobrar")
            print("0. Salir del sistema")

            codigo = input("\nCódigo de barras o número de opción: ").strip()

            # 🧭 Opciones del menú
            if codigo == "0":
                print("👋 Saliendo del sistema...")
                return

            elif codigo == "3":
                break  # 👉 Finalizar la venta actual

            elif codigo == "2":
                print("\n=== TOTAL ACTUAL ===")
                print(f"Total acumulado: ${float(total):.2f}")
                continue

            elif codigo == "1" or codigo.isdigit() or len(codigo) >= 6:
                producto = buscar_producto_por_codigo(codigo)
                if not producto:
                    print("❌ Producto no encontrado.")
                    continue

                id_prod, nombre, precio, stock = producto
                print(f"{nombre} - ${float(precio):.2f} | Stock: {stock}")

                try:
                    cantidad = int(input("Cantidad: "))
                    if cantidad <= 0:
                        print("Cantidad inválida.")
                        continue
                    if cantidad > stock:
                        print("Stock insuficiente.")
                        continue
                except ValueError:
                    print("Ingrese una cantidad válida.")
                    continue

                subtotal = precio * Decimal(cantidad)
                total += subtotal
                venta.append((id_prod, nombre, cantidad, subtotal))

                print(f"{cantidad} x {nombre} agregado. Subtotal: ${float(subtotal):.2f}")
                # 👇 Ya no pedimos Enter aquí, vuelve al inicio del loop para otro producto
                continue

            else:
                print("⚠️ Opción no válida. Intente de nuevo.")
                continue

        # === Finalizar venta ===
        if total > 0:
            print("\n=== RESUMEN DE VENTA ===")
            for item in venta:
                print(f"{item[2]} x {item[1]} = ${float(item[3]):.2f}")
            print(f"\nTOTAL: ${float(total):.2f}")

            # 💰 Cobro
            while True:
                try:
                    dinero = float(input("\nIngrese dinero recibido: $"))
                    if dinero < float(total):
                        print("Dinero insuficiente. Ingrese un monto mayor o igual al total.")
                    else:
                        break
                except ValueError:
                    print("Ingrese un número válido.")

            cambio = float(dinero) - float(total)
            print(f"\nCambio a devolver: ${cambio:.2f}")

            
            id_venta = registrar_venta(float(total))
            for item in venta:
                registrar_venta_detalle(id_venta, item[0], item[2], float(item[3]))

            print("\n Venta registrada correctamente.")
            print("===================================")
            input("Presione Enter para continuar...")

        else:
            print("\nNo se registraron productos en esta venta.")
