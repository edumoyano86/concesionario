from datetime import date, timedelta
from rich.console import Console
from rich.table import Table
import datos

console = Console(color_system="standard")

def ok(msg):    console.print(f"[green]✅ {msg}[/]")
def error(msg): console.print(f"[red]❌ {msg}[/]")
def aviso(msg): console.print(f"[yellow]⚠️  {msg}[/]")
def info(msg):  console.print(f"[cyan]🔍 {msg}[/]")

def _formatear_precio(valor):
    return f"${valor:,}".replace(",", ".")

#   MENÚ

def menu_reservas(datos_actualizados):
    while True:
        console.print(f"\n[bold blue]══════════════════════════════════════[/]")
        console.print(f"[bold blue]  📌 RESERVAS[/]")
        console.print(f"[bold blue]══════════════════════════════════════[/]")
        console.print(f"  [cyan]1.[/] Registrar una reserva nueva")
        console.print(f"  [cyan]2.[/] Ver reservas activas")
        console.print(f"  [cyan]3.[/] Buscar una reserva")
        console.print(f"  [cyan]4.[/] Convertir una reserva en venta")
        console.print(f"  [cyan]5.[/] Cancelar una reserva")
        console.print(f"  [bright_black]9. Volver al menú principal[/]")
        console.print(f"[blue]══════════════════════════════════════[/]")
        opcion = console.input(f"[white]¿Qué querés hacer? [/]").strip()

        if opcion == "1":
            registrar_reserva(datos_actualizados)
            datos.guardar_todo(datos_actualizados)
        elif opcion == "2":
            ver_reservas_activas(datos_actualizados)
        elif opcion == "3":
            buscar_reserva(datos_actualizados)
        elif opcion == "4":
            convertir_en_venta(datos_actualizados)
            datos.guardar_todo(datos_actualizados)
        elif opcion == "5":
            cancelar_reserva(datos_actualizados)
            datos.guardar_todo(datos_actualizados)
        elif opcion == "9":
            break
        else:
            aviso("Opción inválida, intentá de nuevo.")

#   REGISTRAR RESERVA

def registrar_reserva(datos_actualizados):
    lista_reservas = datos_actualizados.get("reservas", [])
    lista_autos = datos_actualizados.get("autos", [])
    lista_clientes = datos_actualizados.get("clientes", [])
    lista_vendedores = datos_actualizados.get("vendedores", [])

    if not lista_autos:
        aviso("No hay autos disponibles para reservar.")
        return
    if not lista_clientes:
        aviso("No hay clientes registrados.")
        return
    if not lista_vendedores:
        aviso("No hay vendedores registrados.")
        return

    tablas_autos = Table(title="Autos disponibles")
    tablas_autos.add_column("ID", justify="center")
    tablas_autos.add_column("Patente", justify="center")
    tablas_autos.add_column("Marca", justify="center")
    tablas_autos.add_column("Modelo", justify="center")
    tablas_autos.add_column("Año", justify="center")
    tablas_autos.add_column("Km", justify="center")
    tablas_autos.add_column("Precio", justify="center")
    tablas_autos.add_column("Estado", justify="center")

    autos_disponibles = 0
    for auto in lista_autos:
        if auto.get("estado") == "disponible":
            autos_disponibles = autos_disponibles + 1
            tablas_autos.add_row(
                str(auto.get("id", "")),
                auto.get("patente", ""),
                auto.get("marca", ""),
                auto.get("modelo", ""),
                str(auto.get("anio", "")),
                str(auto.get("kilometros", "")),
                _formatear_precio(auto.get("precio", 0)),
                auto.get("estado", "")
            )
    if autos_disponibles == 0:
        aviso("No hay autos disponibles para reservar.")
        return
    console.print(tablas_autos)

    id_auto_str = input("Ingrese el ID del auto a reservar: ")
    if not id_auto_str.isdigit():
        aviso("ID inválido.")
        return
    id_auto = int(id_auto_str)

    auto_encontrado = None
    for auto in lista_autos:
        if auto.get("id") == id_auto:
            auto_encontrado = auto
            break
    if not auto_encontrado:
        aviso("Auto no encontrado.")
        return
    
    if auto_encontrado.get("estado") != "disponible":
        aviso(f"El auto está en estado '{auto_encontrado.get('estado')}', no se puede reservar.")
        return

    tablas_clientes = Table(title="Clientes")
    tablas_clientes.add_column("ID", justify="center")
    tablas_clientes.add_column("Nombre", justify="center")
    tablas_clientes.add_column("Apellido", justify="center")
    tablas_clientes.add_column("DNI", justify="center")
    tablas_clientes.add_column("Email", justify="center")
    tablas_clientes.add_column("Teléfono", justify="center")

    for cliente in lista_clientes:
        tablas_clientes.add_row(
            str(cliente.get("id_interno", "")),
            cliente.get("nombre", ""),
            cliente.get("apellido", ""),
            cliente.get("dni", ""),
            cliente.get("email", ""),
            cliente.get("telefono", "")
        )
    console.print(tablas_clientes)

    id_cliente_str = input("Ingrese el ID del cliente: ")
    if not id_cliente_str.isdigit():
        aviso("ID inválido.")
        return
    id_cliente = int(id_cliente_str)

    cliente_encontrado = None
    for cliente in lista_clientes:
        if cliente.get("id_interno") == id_cliente:
            cliente_encontrado = cliente
            break
    if not cliente_encontrado:
        aviso("Cliente no encontrado.")
        return

    tablas_vendedores = Table(title="Vendedores")
    tablas_vendedores.add_column("ID", justify="center")
    tablas_vendedores.add_column("Nombre", justify="center")
    tablas_vendedores.add_column("Comisión", justify="center")

    for vendedor in lista_vendedores:
        if vendedor.get("estado") == "activo":
            tablas_vendedores.add_row(
                str(vendedor.get("id", "")),
                vendedor.get("nombre_completo", ""),
                str(vendedor.get("comision_porcentaje", "")) + "%"
            )
    console.print(tablas_vendedores)

    id_vendedor_str = input("Ingrese el ID del vendedor: ")
    if not id_vendedor_str.isdigit():
        aviso("ID inválido.")
        return
    id_vendedor = int(id_vendedor_str)

    vendedor_encontrado = None
    for vendedor in lista_vendedores:
        if vendedor.get("id") == id_vendedor:
            vendedor_encontrado = vendedor
            break
    if not vendedor_encontrado:
        aviso("Vendedor no encontrado.")
        return

    monto_sena_str = input("Ingrese el monto de la seña: ")
    if not monto_sena_str.isdigit():
        aviso("El monto debe ser un número entero.")
        return
    monto_sena = int(monto_sena_str)

    dias_plazo_str = input("Ingrese los días de plazo para concretar la compra: ")
    if not dias_plazo_str.isdigit():
        aviso("Los días deben ser un número entero.")
        return
    dias_plazo = int(dias_plazo_str)
    fecha_limite = (date.today() + timedelta(days=dias_plazo)).isoformat()

    nuevo_id = 1
    for r in lista_reservas:
        if r["id"] >= nuevo_id:
            nuevo_id = r["id"] + 1

    reserva = {
        "id": nuevo_id,
        "id_auto": id_auto,
        "id_cliente": id_cliente,
        "id_vendedor": id_vendedor,
        "fecha_reserva": date.today().isoformat(),
        "monto_sena": monto_sena,
        "fecha_limite": fecha_limite,
        "estado": "activa"
    }

    auto_encontrado["estado"] = "reservado"

    lista_reservas.append(reserva)
    ok(f"Reserva #{nuevo_id} creada exitosamente. El auto pasó a 'reservado'.")

#   VER RESERVAS ACTIVAS

def ver_reservas_activas(datos_actualizados):
    lista_reservas = datos_actualizados.get("reservas", [])
    reservas_activas = [r for r in lista_reservas if r.get("estado") == "activa"]
    if not reservas_activas:
        aviso("No hay reservas activas registradas.")
        return

    tablas_reservas = Table(title="Reservas Activas")
    tablas_reservas.add_column("ID", justify="center")
    tablas_reservas.add_column("ID Auto", justify="center")
    tablas_reservas.add_column("ID Cliente", justify="center")
    tablas_reservas.add_column("ID Vendedor", justify="center")
    tablas_reservas.add_column("Fecha Reserva", justify="center")
    tablas_reservas.add_column("Seña", justify="center")
    tablas_reservas.add_column("Fecha Límite", justify="center")
    tablas_reservas.add_column("Estado", justify="center")

    for reserva in reservas_activas:
        tablas_reservas.add_row(
            str(reserva.get("id", "")),
            str(reserva.get("id_auto", "")),
            str(reserva.get("id_cliente", "")),
            str(reserva.get("id_vendedor", "")),
            reserva.get("fecha_reserva", ""),
            _formatear_precio(reserva.get("monto_sena", 0)),
            reserva.get("fecha_limite", ""),
            reserva.get("estado", "")
        )
    console.print(tablas_reservas)

#   BUSCAR RESERVA

def _mostrar_tabla_reservas(reservas, autos, clientes, vendedores):
    if not reservas:
        aviso("No se encontraron reservas.")
        return
    tabla = Table(title="Resultados de búsqueda")
    tabla.add_column("ID", justify="center")
    tabla.add_column("Auto", justify="center")
    tabla.add_column("Cliente", justify="center")
    tabla.add_column("Vendedor", justify="center")
    tabla.add_column("Fecha Reserva", justify="center")
    tabla.add_column("Seña", justify="center")
    tabla.add_column("Fecha Límite", justify="center")
    tabla.add_column("Estado", justify="center")

    for r in reservas:
        auto = next((a for a in autos if a.get("id") == r.get("id_auto")), None)
        cliente = next((c for c in clientes if c.get("id_interno") == r.get("id_cliente")), None)
        vendedor = next((v for v in vendedores if v.get("id") == r.get("id_vendedor")), None)

        auto_label = f"{auto.get('marca','')} {auto.get('modelo','')} ({auto.get('patente','')})" if auto else f"ID {r.get('id_auto')}"
        cliente_label = f"{cliente.get('nombre','')} {cliente.get('apellido','')}" if cliente else f"ID {r.get('id_cliente')}"
        vendedor_label = vendedor.get("nombre_completo", f"ID {r.get('id_vendedor')}") if vendedor else f"ID {r.get('id_vendedor')}"

        tabla.add_row(
            str(r.get("id", "")),
            auto_label,
            cliente_label,
            vendedor_label,
            r.get("fecha_reserva", ""),
            _formatear_precio(r.get("monto_sena", 0)),
            r.get("fecha_limite", ""),
            r.get("estado", "")
        )
    console.print(tabla)

def _buscar_por_auto(datos_actualizados):
    lista_autos = datos_actualizados.get("autos", [])
    lista_reservas = datos_actualizados.get("reservas", [])
    if not lista_reservas:
        aviso("No hay reservas registradas.")
        return

    autos_reservados = [a for a in lista_autos if a.get("estado") == "reservado"]
    if not autos_reservados:
        aviso("No hay autos reservados.")
        return
    tabla = Table(title="Autos con reserva activa")
    tabla.add_column("ID", justify="center")
    tabla.add_column("Patente", justify="center")
    tabla.add_column("Marca", justify="center")
    tabla.add_column("Modelo", justify="center")
    for auto in autos_reservados:
        tabla.add_row(str(auto.get("id","")), auto.get("patente",""), auto.get("marca",""), auto.get("modelo",""))
    console.print(tabla)

    id_str = input("Ingrese el ID del auto: ")
    if not id_str.isdigit():
        aviso("ID inválido.")
        return
    id_auto = int(id_str)
    encontradas = [r for r in lista_reservas if r.get("id_auto") == id_auto]
    _mostrar_tabla_reservas(encontradas, lista_autos, datos_actualizados.get("clientes",[]), datos_actualizados.get("vendedores",[]))

def _buscar_por_cliente(datos_actualizados):
    lista_clientes = datos_actualizados.get("clientes", [])
    lista_reservas = datos_actualizados.get("reservas", [])
    if not lista_reservas:
        aviso("No hay reservas registradas.")
        return

    tabla = Table(title="Clientes")
    tabla.add_column("ID", justify="center")
    tabla.add_column("Nombre", justify="center")
    tabla.add_column("Apellido", justify="center")
    tabla.add_column("DNI", justify="center")
    for c in lista_clientes:
        tabla.add_row(str(c.get("id_interno","")), c.get("nombre",""), c.get("apellido",""), c.get("dni",""))
    console.print(tabla)

    id_str = input("Ingrese el ID del cliente: ")
    if not id_str.isdigit():
        aviso("ID inválido.")
        return
    id_cliente = int(id_str)
    encontradas = [r for r in lista_reservas if r.get("id_cliente") == id_cliente]
    _mostrar_tabla_reservas(encontradas, datos_actualizados.get("autos",[]), lista_clientes, datos_actualizados.get("vendedores",[]))

def _buscar_por_vendedor(datos_actualizados):
    lista_vendedores = datos_actualizados.get("vendedores", [])
    lista_reservas = datos_actualizados.get("reservas", [])
    if not lista_reservas:
        aviso("No hay reservas registradas.")
        return

    tabla = Table(title="Vendedores")
    tabla.add_column("ID", justify="center")
    tabla.add_column("Nombre", justify="center")
    for v in lista_vendedores:
        tabla.add_row(str(v.get("id","")), v.get("nombre_completo",""))
    console.print(tabla)

    id_str = input("Ingrese el ID del vendedor: ")
    if not id_str.isdigit():
        aviso("ID inválido.")
        return
    id_vendedor = int(id_str)
    encontradas = [r for r in lista_reservas if r.get("id_vendedor") == id_vendedor]
    _mostrar_tabla_reservas(encontradas, datos_actualizados.get("autos",[]), datos_actualizados.get("clientes",[]), lista_vendedores)

def buscar_reserva(datos_actualizados):
    while True:
        console.print(f"\n[bold blue]══════════════════════════════════════[/]")
        console.print(f"[bold blue]  🔍 BUSCAR RESERVAS POR AUTO, POR CLIENTE O POR VENDEDOR[/]")
        console.print(f"[bold blue]══════════════════════════════════════[/]")
        console.print(f"  [cyan]1.[/] Buscar por auto")
        console.print(f"  [cyan]2.[/] Buscar por cliente")
        console.print(f"  [cyan]3.[/] Buscar por vendedor")
        console.print(f"  [bright_black]9. Volver al menú de reservas[/]")
        console.print(f"[blue]══════════════════════════════════════[/]")
        opcion = console.input("[white]Elegí una opción: [/]").strip()

        if opcion == "1":
            _buscar_por_auto(datos_actualizados)
        elif opcion == "2":
            _buscar_por_cliente(datos_actualizados)
        elif opcion == "3":
            _buscar_por_vendedor(datos_actualizados)
        elif opcion == "9":
            break
        else:
            aviso("Opción inválida, intentá de nuevo.")

#   CONVERTIR EN VENTA

def convertir_en_venta(datos_actualizados):
    lista_reservas = datos_actualizados.get("reservas", [])
    lista_autos = datos_actualizados.get("autos", [])
    lista_ventas = datos_actualizados.get("ventas", [])

    reservas_activas = [r for r in lista_reservas if r.get("estado") == "activa"]
    if not reservas_activas:
        aviso("No hay reservas activas para convertir en venta.")
        return

    id_reserva_str = input("Ingrese el ID de la reserva: ")
    if not id_reserva_str.isdigit():
        aviso("ID inválido.")
        return
    id_reserva = int(id_reserva_str)

    reserva_encontrada = None
    for reserva in lista_reservas:
        if reserva.get("id") == id_reserva:
            reserva_encontrada = reserva
            break
    if not reserva_encontrada:
        aviso("Reserva no encontrada.")
        return

    if reserva_encontrada.get("estado") != "activa":
        aviso(f"Esta reserva ya está '{reserva_encontrada.get('estado')}', no se puede convertir.")
        return

    auto_encontrado = None
    for auto in lista_autos:
        if auto.get("id") == reserva_encontrada.get("id_auto"):
            auto_encontrado = auto
            break
    if auto_encontrado:
        if auto_encontrado.get("estado") == "reservado":
            auto_encontrado["estado"] = "vendido"
        else:
            aviso(f"El auto está en estado '{auto_encontrado.get('estado')}', no se cambió a vendido.")

    nuevo_id_venta = 1
    for v in lista_ventas:
        if v["id"] >= nuevo_id_venta:
            nuevo_id_venta = v["id"] + 1

    venta = {
        "id": nuevo_id_venta,
        "id_auto": reserva_encontrada["id_auto"],
        "id_cliente": reserva_encontrada["id_cliente"],
        "id_vendedor": reserva_encontrada["id_vendedor"],
        "fecha_venta": date.today().isoformat(),
        "precio_final": auto_encontrado.get("precio", 0) if auto_encontrado else 0,
        "forma_pago": "contado",
        "estado_pago": "cobrado"
    }
    lista_ventas.append(venta)

    reserva_encontrada["estado"] = "concretada"
    ok(f"Reserva convertida en venta #{nuevo_id_venta} exitosamente. El auto pasó a 'vendido'.")

#   CANCELAR RESERVA

def cancelar_reserva(datos_actualizados):
    lista_reservas = datos_actualizados.get("reservas", [])
    lista_autos = datos_actualizados.get("autos", [])

    if not lista_reservas:
        aviso("No hay reservas registradas.")
        return

    id_reserva_str = input("Ingrese el ID de la reserva: ")
    if not id_reserva_str.isdigit():
        aviso("ID inválido.")
        return
    id_reserva = int(id_reserva_str)

    reserva_encontrada = None
    for reserva in lista_reservas:
        if reserva.get("id") == id_reserva:
            reserva_encontrada = reserva
            break
    if not reserva_encontrada:
        aviso("Reserva no encontrada.")
        return

    if reserva_encontrada.get("estado") != "activa":
        aviso("Esta reserva ya fue procesada y no se puede cancelar.")
        return

    auto_encontrado = None
    for auto in lista_autos:
        if auto.get("id") == reserva_encontrada.get("id_auto"):
            auto_encontrado = auto
            break
    if auto_encontrado:
        if auto_encontrado.get("estado") == "reservado":
            auto_encontrado["estado"] = "disponible"
        else:
            aviso(f"El auto está en estado '{auto_encontrado.get('estado')}', no se cambió a disponible.")

    reserva_encontrada["estado"] = "cancelada"
    ok("Reserva cancelada exitosamente. El auto vuelve a estar 'disponible'.")