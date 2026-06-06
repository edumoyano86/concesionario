# ventas.py
import json
import os
from datetime import date
from colores import *

# ─── CONFIGURACIÓN DEL ARCHIVO JSON ───────────────────────────────────────────
ARCHIVO_JSON = "ventas.json"



# ─── FUNCIONES DE PERSISTENCIA JSON ───────────────────────────────────────────

def cargar_datos():
    """
    Carga todos los datos desde ventas.json.
    Si el archivo no existe, lo crea con una estructura vacía.
    Retorna un diccionario con claves: autos, clientes, vendedores, ventas.
    """
    if not os.path.exists(ARCHIVO_JSON):
        datos_vacios = {
            "autos": [],
            "clientes": [],
            "vendedores": [],
            "ventas": []
        }
        print(f"{AMARILLO_B}⚠  No se encontró '{ARCHIVO_JSON}'. Creando archivo nuevo vacío...{RESET}")
        guardar_datos(datos_vacios)
        return datos_vacios

    with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    print(f"{DIM}  ✔ Datos cargados desde '{ARCHIVO_JSON}'.{RESET}")
    return datos


def guardar_datos(datos):
    """
    Guarda el diccionario completo (autos, clientes, vendedores, ventas) en ventas.json.
    Las fechas tipo date se convierten a string 'YYYY-MM-DD' automáticamente.
    """
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False, default=str)


# ─── FUNCIÓN AUXILIAR ─────────────────────────────────────────────────────────

def pedir_dato(mensaje):
    """Pide un dato al usuario con estilo en la terminal"""
    return input(f"{CYAN_B}  ▶  {mensaje}: {RESET}").strip()


# ─── MENÚ PRINCIPAL DE VENTAS ─────────────────────────────────────────────────

def mostrar_menu_ventas(lista_ventas=None, lista_autos=None, lista_clientes=None, lista_vendedores=None):
    """
    Maneja el menú interactivo de ventas en consola.
    Carga los datos desde JSON al entrar y los guarda después de cada operación.
    Los parámetros opcionales se ignoran: siempre trabaja con el JSON propio.
    """
    # Cargamos SIEMPRE desde el JSON al entrar al módulo
    datos = cargar_datos()

    while True:
        ancho = 50
        print()
        print(f"{DIM}{CYAN}{'═' * ancho}{RESET}")
        print(f"{BOLD}{AZUL_B}{'💰  ÁREA DE VENTAS':^{ancho}}{RESET}")
        print(f"{DIM}{CYAN}{'═' * ancho}{RESET}")
        print()
        print(f"  {CYAN}[1]{RESET} {BLANCO_B}Registrar una venta nueva{RESET}")
        print(f"  {CYAN}[2]{RESET} {BLANCO_B}Ver todas las ventas{RESET}")
        print(f"  {CYAN}[3]{RESET} {BLANCO_B}Buscar venta{RESET}  {DIM}(por Patente, DNI o Vendedor){RESET}")
        print(f"  {CYAN}[4]{RESET} {BLANCO_B}Modificar estado de pago{RESET}")
        print(f"  {CYAN}[5]{RESET} {BLANCO_B}Eliminar / Anular una venta{RESET}")
        print(f"  {CYAN}[6]{RESET} {BLANCO_B}Consultar comisiones de Vendedores{RESET}")
        print()
        print(f"  {AMARILLO}[9]{RESET} {DIM}Volver al Menú Principal{RESET}")
        print()
        print(f"{DIM}{CYAN}{'─' * ancho}{RESET}")

        opcion_sel = pedir_dato("Seleccione una opción")

        if not opcion_sel:
            break

        match opcion_sel:
            case "1":
                registrar_venta(datos)
                guardar_datos(datos)
            case "2":
                listar_ventas(datos)
            case "3":
                buscar_venta(datos)
            case "4":
                modificar_estado_pago(datos["ventas"])
                guardar_datos(datos)
            case "5":
                eliminar_venta(datos)
                guardar_datos(datos)
            case "6":
                calcular_comisiones(datos["ventas"], datos["vendedores"])
            case "9":
                print()
                print(f"{VERDE_B}✅ Volviendo al menú principal...{RESET}")
                break
            case _:
                print()
                print(f"{AMARILLO_B}⚠  Opción inválida. Intente de nuevo.{RESET}")


# ─── OPERACIONES CRUD ─────────────────────────────────────────────────────────

def registrar_venta(datos):
    """Registra una nueva venta. Recibe el dict completo de datos."""
    lista_ventas    = datos["ventas"]
    lista_autos     = datos["autos"]
    lista_clientes  = datos["clientes"]
    lista_vendedores = datos["vendedores"]

    print()
    print(f"{BOLD}{AZUL_B}─── REGISTRAR NUEVA VENTA ───{RESET}")

    # Mostrar autos disponibles para orientar al usuario
    print()
    print(f"  {DIM}Autos disponibles:{RESET}")
    disponibles = [a for a in lista_autos if a["estado"] == "disponible"]
    if not disponibles:
        print(f"  {AMARILLO_B}⚠  No hay autos disponibles en este momento.{RESET}")
        return
    for a in disponibles:
        print(f"  {CYAN}ID {a['id']}{RESET} - {BLANCO_B}{a['marca']} {a['modelo']} ({a['anio']}){RESET}  "
              f"Patente: {DIM}{a['patente']}{RESET}  Precio: {VERDE_B}${a['precio']}{RESET}")
    print()

    id_auto_str = pedir_dato("ID del auto a vender")
    try:
        id_auto = int(id_auto_str)
    except (ValueError, TypeError):
        print(f"{ROJO_B}❌ El ID debe ser un número entero.{RESET}")
        return

    auto_encontrado = None
    for auto in lista_autos:
        if auto["id"] == id_auto:
            auto_encontrado = auto
            break

    if not auto_encontrado:
        print(f"{ROJO_B}❌ El ID de auto no existe en el stock.{RESET}")
        return

    if auto_encontrado["estado"] == "vendido":
        print(f"{ROJO_B}❌ Este auto ya fue vendido previamente.{RESET}")
        return

    # Mostrar clientes disponibles
    print()
    print(f"  {DIM}Clientes registrados:{RESET}")
    for c in lista_clientes:
        print(f"  {CYAN}ID {c['id']}{RESET} - {BLANCO_B}{c['nombre_completo']}{RESET}  DNI: {DIM}{c['dni']}{RESET}")
    print()

    id_cliente_str = pedir_dato("ID del cliente")
    try:
        id_cliente = int(id_cliente_str)
    except (ValueError, TypeError):
        print(f"{ROJO_B}❌ El ID debe ser un número entero.{RESET}")
        return

    cliente_existe = any(c["id"] == id_cliente for c in lista_clientes)
    if not cliente_existe:
        print(f"{ROJO_B}❌ El cliente no está registrado en la base de datos.{RESET}")
        return

    # Mostrar vendedores disponibles
    print()
    print(f"  {DIM}Vendedores activos:{RESET}")
    for v in lista_vendedores:
        if v["estado"] == "activo":
            print(f"  {CYAN}ID {v['id']}{RESET} - {BLANCO_B}{v['nombre_completo']}{RESET}  "
                  f"Comisión: {AMARILLO_B}{v['comision_porcentaje']}%{RESET}")
    print()

    id_vendedor_str = pedir_dato("ID del vendedor")
    try:
        id_vendedor = int(id_vendedor_str)
    except (ValueError, TypeError):
        print(f"{ROJO_B}❌ El ID debe ser un número entero.{RESET}")
        return

    vendedor_existe = any(v["id"] == id_vendedor for v in lista_vendedores)
    if not vendedor_existe:
        print(f"{ROJO_B}❌ El vendedor no existe en el equipo.{RESET}")
        return

    precio_str = pedir_dato(f"Precio final acordado (Precio lista ${auto_encontrado['precio']})")
    try:
        precio_final = int(precio_str)
    except (ValueError, TypeError):
        print(f"{ROJO_B}❌ El precio debe ser un número entero.{RESET}")
        return

    forma_pago = pedir_dato("Forma de pago (contado / financiado / parte de pago)")
    forma_pago = forma_pago.strip().lower() if forma_pago else ""

    estado_pago = pedir_dato("Estado del pago (cobrado / pendiente / en cuotas)")
    estado_pago = estado_pago.strip().lower() if estado_pago else ""

    # Actualizar estado del auto
    auto_encontrado["estado"] = "vendido"

    # Calcular ID incremental
    nuevo_id = max((v["id"] for v in lista_ventas), default=0) + 1

    nueva_venta = {
        "id": nuevo_id,
        "id_auto": id_auto,
        "id_cliente": id_cliente,
        "id_vendedor": id_vendedor,
        "fecha_venta": str(date.today()),   # guardamos como string 'YYYY-MM-DD'
        "precio_final": precio_final,
        "forma_pago": forma_pago,
        "estado_pago": estado_pago
    }

    lista_ventas.append(nueva_venta)
    print()
    print(f"{VERDE_B}✅ ¡Venta registrada! El auto {BLANCO_B}{auto_encontrado['marca']} {auto_encontrado['modelo']}{RESET} "
          f"{VERDE_B}ahora figura como VENDIDO.{RESET}")


def listar_ventas(datos):
    """Muestra el historial completo de ventas con nombres reales (no solo IDs)."""
    lista_ventas     = datos["ventas"]
    lista_autos      = datos["autos"]
    lista_clientes   = datos["clientes"]
    lista_vendedores = datos["vendedores"]

    print()
    if not lista_ventas:
        print(f"{AMARILLO_B}⚠  No hay ventas registradas en el sistema todavía.{RESET}")
        return

    print(f"{BOLD}{AZUL_B}─── HISTORIAL DE VENTAS ({len(lista_ventas)} registros) ───{RESET}")
    print()

    for v in lista_ventas:
        # Buscar los nombres a partir de los IDs guardados
        auto     = next((a for a in lista_autos      if a["id"] == v["id_auto"]),     None)
        cliente  = next((c for c in lista_clientes   if c["id"] == v["id_cliente"]),  None)
        vendedor = next((vd for vd in lista_vendedores if vd["id"] == v["id_vendedor"]), None)

        nombre_auto     = f"{auto['marca']} {auto['modelo']} ({auto['patente']})" if auto     else f"Auto ID {v['id_auto']} (no encontrado)"
        nombre_cliente  = cliente["nombre_completo"]                                if cliente  else f"Cliente ID {v['id_cliente']}"
        nombre_vendedor = vendedor["nombre_completo"]                               if vendedor else f"Vendedor ID {v['id_vendedor']}"

        ancho = 54
        print(f"  {DIM}{CYAN}{'─' * ancho}{RESET}")
        print(f"  {CYAN_B}Venta #{v['id']}{RESET}  {DIM}——{RESET}  Fecha: {BLANCO_B}{v['fecha_venta']}{RESET}")
        print(f"    🚗  Auto:      {BLANCO_B}{nombre_auto}{RESET}")
        print(f"    👤  Cliente:   {BLANCO_B}{nombre_cliente}{RESET}")
        print(f"    🧑‍💼  Vendedor:  {BLANCO_B}{nombre_vendedor}{RESET}")
        print(f"    💰  Total:     {VERDE_B}${v['precio_final']:,}{RESET}   "
              f"Pago: {AMARILLO_B}{v['forma_pago']}{RESET}   "
              f"Estado: {AMARILLO_B}{v['estado_pago']}{RESET}")
    print(f"  {DIM}{CYAN}{'─' * ancho}{RESET}")


def buscar_venta(datos):
    lista_ventas   = datos["ventas"]
    lista_autos    = datos["autos"]
    lista_clientes = datos["clientes"]

    print()
    print(f"{BOLD}{AZUL_B}─── OPCIONES DE BÚSQUEDA ───{RESET}")
    print(f"  {CYAN}[1]{RESET} Buscar por Patente del auto")
    print(f"  {CYAN}[2]{RESET} Buscar por DNI del cliente")
    print(f"  {CYAN}[3]{RESET} Buscar por ID del Vendedor")
    print()

    opcion_bus = pedir_dato("Seleccione opción de búsqueda (1, 2 o 3)")
    if not opcion_bus:
        return
    opcion_bus = opcion_bus.strip()
    encontrado = False

    match opcion_bus:
        case "1":
            patente_buscar = pedir_dato("Ingrese la patente del auto")
            if not patente_buscar:
                return
            patente_buscar = patente_buscar.strip().upper()

            id_auto_encontrado = None
            for auto in lista_autos:
                if auto["patente"].upper() == patente_buscar:
                    id_auto_encontrado = auto["id"]
                    break

            if id_auto_encontrado:
                for v in lista_ventas:
                    if v["id_auto"] == id_auto_encontrado:
                        _imprimir_venta(v, datos)
                        encontrado = True

        case "2":
            dni_buscar = pedir_dato("Ingrese el DNI del cliente")
            if not dni_buscar:
                return
            dni_buscar = dni_buscar.strip()

            id_cliente_encontrado = None
            for cliente in lista_clientes:
                if cliente["dni"] == dni_buscar:
                    id_cliente_encontrado = cliente["id"]
                    break

            if id_cliente_encontrado:
                for v in lista_ventas:
                    if v["id_cliente"] == id_cliente_encontrado:
                        _imprimir_venta(v, datos)
                        encontrado = True

        case "3":
            id_vendedor_str = pedir_dato("Ingrese el ID del vendedor")
            try:
                id_vendedor_buscar = int(id_vendedor_str)
            except (ValueError, TypeError):
                print(f"{ROJO_B}❌ ID inválido.{RESET}")
                return

            for v in lista_ventas:
                if v["id_vendedor"] == id_vendedor_buscar:
                    _imprimir_venta(v, datos)
                    encontrado = True

        case _:
            print(f"{ROJO_B}❌ Opción de búsqueda inválida.{RESET}")
            return

    if not encontrado:
        print(f"{ROJO_B}❌ No se encontró ninguna venta con los criterios ingresados.{RESET}")


def _imprimir_venta(v, datos=None):
    """Helper para imprimir una venta con formato. Si recibe datos, muestra nombres reales."""
    print()
    if datos:
        auto     = next((a  for a  in datos["autos"]      if a["id"]  == v["id_auto"]),     None)
        cliente  = next((c  for c  in datos["clientes"]   if c["id"]  == v["id_cliente"]),  None)
        vendedor = next((vd for vd in datos["vendedores"] if vd["id"] == v["id_vendedor"]), None)
        nombre_auto     = f"{auto['marca']} {auto['modelo']} ({auto['patente']})" if auto     else f"ID {v['id_auto']}"
        nombre_cliente  = cliente["nombre_completo"]                               if cliente  else f"ID {v['id_cliente']}"
        nombre_vendedor = vendedor["nombre_completo"]                              if vendedor else f"ID {v['id_vendedor']}"
    else:
        nombre_auto     = f"Auto ID {v['id_auto']}"
        nombre_cliente  = f"Cliente ID {v['id_cliente']}"
        nombre_vendedor = f"Vendedor ID {v['id_vendedor']}"

    print(f"  {VERDE_B}╔══ VENTA ENCONTRADA — #{v['id']} ══╗{RESET}")
    print(f"  🚗  Auto:      {BLANCO_B}{nombre_auto}{RESET}")
    print(f"  👤  Cliente:   {BLANCO_B}{nombre_cliente}{RESET}")
    print(f"  🧑‍💼  Vendedor:  {BLANCO_B}{nombre_vendedor}{RESET}")
    print(f"  📅  Fecha:     {BLANCO_B}{v['fecha_venta']}{RESET}")
    print(f"  💰  Monto:     {VERDE_B}${v['precio_final']:,}{RESET}   "
          f"Pago: {AMARILLO_B}{v['forma_pago']}{RESET}   "
          f"Estado: {AMARILLO_B}{v['estado_pago']}{RESET}")


def modificar_estado_pago(lista_ventas):
    print()
    print(f"{BOLD}{AZUL_B}─── MODIFICAR ESTADO DE PAGO ───{RESET}")

    id_buscar_str = pedir_dato("Ingrese el número (ID) de la venta")
    try:
        id_buscar = int(id_buscar_str)
    except (ValueError, TypeError):
        print(f"{ROJO_B}❌ Debe ingresar un número.{RESET}")
        return

    for v in lista_ventas:
        if v["id"] == id_buscar:
            print(f"{AZUL_B}🔹 Venta encontrada. Estado actual: {AMARILLO_B}{v['estado_pago']}{RESET}")
            nuevo_estado = pedir_dato("Nuevo estado (cobrado / pendiente / en cuotas)")
            if nuevo_estado:
                v["estado_pago"] = nuevo_estado.strip().lower()
                print(f"{VERDE_B}✅ Estado de pago actualizado con éxito.{RESET}")
            return

    print(f"{ROJO_B}❌ No se encontró ninguna venta con ese número.{RESET}")


def eliminar_venta(datos):
    lista_ventas = datos["ventas"]
    lista_autos  = datos["autos"]

    print()
    print(f"{BOLD}{AZUL_B}─── ANULAR / ELIMINAR VENTA ───{RESET}")

    id_buscar_str = pedir_dato("Ingrese el ID de la venta que desea ANULAR")
    try:
        id_buscar = int(id_buscar_str)
    except (ValueError, TypeError):
        print(f"{ROJO_B}❌ Debe ingresar un número.{RESET}")
        return

    for i, v in enumerate(lista_ventas):
        if v["id"] == id_buscar:
            print()
            print(f"{AMARILLO_B}⚠  Está por borrar la Venta #{v['id']} por un monto de ${v['precio_final']}.{RESET}")
            confirmacion = pedir_dato("¿Está seguro? Escriba S para confirmar")

            if confirmacion and confirmacion.strip().upper() == "S":
                id_auto = v["id_auto"]
                for auto in lista_autos:
                    if auto["id"] == id_auto:
                        auto["estado"] = "disponible"
                        break
                lista_ventas.pop(i)
                print(f"{VERDE_B}✅ Venta anulada. El auto vuelve a figurar como 'disponible'.{RESET}")
                return
            else:
                print(f"{AZUL_B}🔹 Operación cancelada. No se borró ningún dato.{RESET}")
                return

    print(f"{ROJO_B}❌ No se encontró ninguna venta con ese número.{RESET}")


def calcular_comisiones(lista_ventas, lista_vendedores):
    print()
    print(f"{BOLD}{AZUL_B}─── LIQUIDACIÓN DE COMISIONES ───{RESET}")

    # Mostrar vendedores disponibles con su porcentaje de comisión
    print()
    print(f"  {DIM}Vendedores:{RESET}")
    for v in lista_vendedores:
        print(f"  {CYAN}ID {v['id']}{RESET} - {BLANCO_B}{v['nombre_completo']}{RESET} {DIM}({AMARILLO_B}{v['comision_porcentaje']}%{RESET}{DIM}){RESET}")
    print()

    id_vendedor_str = pedir_dato("Ingrese el ID del vendedor a consultar")
    try:
        id_vendedor = int(id_vendedor_str)
    except (ValueError, TypeError):
        print(f"{ROJO_B}❌ Debe ingresar un número.{RESET}")
        return

    vendedor_encontrado = None
    for v in lista_vendedores:
        if v["id"] == id_vendedor:
            vendedor_encontrado = v
            break

    if not vendedor_encontrado:
        print(f"{ROJO_B}❌ El vendedor no existe.{RESET}")
        return

    print()
    print(f"  {BOLD}{BLANCO_B}Vendedor:{RESET} {BLANCO_B}{vendedor_encontrado['nombre_completo']}{RESET}  "
          f"{DIM}|{RESET}  Comisión asignada: {AMARILLO_B}{vendedor_encontrado['comision_porcentaje']}%{RESET}")
    print(f"{DIM}{CYAN}{'─' * 60}{RESET}")

    total_vendido = 0
    tiene_ventas = False

    for venta in lista_ventas:
        if venta["id_vendedor"] == id_vendedor:
            monto_venta = venta["precio_final"]
            comision_individual = monto_venta * (vendedor_encontrado["comision_porcentaje"] / 100)
            print(f"  {DIM}Venta #{venta['id']}{RESET}  {DIM}|{RESET}  "
                  f"Fecha: {BLANCO_B}{venta['fecha_venta']}{RESET}  {DIM}|{RESET}  "
                  f"Monto: {VERDE_B}${monto_venta:,}{RESET}  {DIM}|{RESET}  "
                  f"Comisión: {AMARILLO_B}${comision_individual:,.2f}{RESET}")
            total_vendido += monto_venta
            tiene_ventas = True

    if not tiene_ventas:
        print(f"  {DIM}Este vendedor aún no registra operaciones.{RESET}")

    comision_final = total_vendido * (vendedor_encontrado["comision_porcentaje"] / 100)
    print(f"{DIM}{CYAN}{'─' * 60}{RESET}")
    print(f"  {BOLD}Total Facturado:        {VERDE_B}${total_vendido:,}{RESET}")
    print(f"  {BOLD}Comisión Total a pagar: {AMARILLO_B}${comision_final:,.2f}{RESET}")


# ─── EJECUCIÓN STANDALONE ─────────────────────────────────────────────────────
# Permite correr ventas.py directamente: python3 ventas.py
# Funciona de forma independiente sin necesitar main.py
if __name__ == "__main__":
    import os
    os.system('clear' if os.name != 'nt' else 'cls')
    print()
    print(f"{BOLD}{ROJO_B}{'🚗  AUTOS DEL LITORAL  🚗':^50}{RESET}")
    print(f"{DIM}{CYAN}{'═' * 50}{RESET}")
    print(f"{DIM}  Modo: Módulo de Ventas (standalone){RESET}")
    mostrar_menu_ventas()