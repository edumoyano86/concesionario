import json
from datetime import date

autos = []
contador_id_autos = 1

ESTADOS_VALIDOS = ("disponible", "reservado", "vendido", "en taller")
ARCHIVO_JSON    = "stock_autos.json"

# ──────────────────────────────────────────────
#  COLORES
# ──────────────────────────────────────────────

VERDE    = "\033[92m"
ROJO     = "\033[91m"
AMARILLO = "\033[93m"
AZUL     = "\033[94m"
CIAN     = "\033[96m"
BLANCO   = "\033[97m"
GRIS     = "\033[90m"
RESET    = "\033[0m"
NEGRITA  = "\033[1m"

def ok(msg):    print(f"{VERDE}✅ {msg}{RESET}")
def error(msg): print(f"{ROJO}❌ {msg}{RESET}")
def aviso(msg): print(f"{AMARILLO}⚠️  {msg}{RESET}")
def info(msg):  print(f"{CIAN}🔍 {msg}{RESET}")


# ──────────────────────────────────────────────
#  JSON
# ──────────────────────────────────────────────

def cargar_desde_json():
    # Lee el archivo JSON y carga los autos en memoria al iniciar.
    global autos, contador_id_autos
    try:
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
            datos = json.load(f)
        for a in datos:
            a["fecha_ingreso"] = date.fromisoformat(a["fecha_ingreso"])  # str → date
        autos = datos
        if autos:
            contador_id_autos = max(a["id"] for a in autos) + 1
    except FileNotFoundError:
        autos = []  # Si no existe el archivo, arranca vacío
    except json.JSONDecodeError:
        aviso("El archivo JSON estaba dañado. Se arranca con lista vacía.")
        autos = []


def guardar_en_json():
    # Guarda el estado actual de la lista en el archivo JSON.
    datos = []
    for a in autos:
        copia = a.copy()
        copia["fecha_ingreso"] = a["fecha_ingreso"].isoformat()  # date → str
        datos.append(copia)
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


# ──────────────────────────────────────────────
#  MENÚ
# ──────────────────────────────────────────────

def menu_autos():
    cargar_desde_json()  # Carga los datos al entrar al módulo
    while True:
        print(f"\n{AZUL}{NEGRITA}══════════════════════════════════════{RESET}")
        print(f"{AZUL}{NEGRITA}  🚗 AUTOS EN STOCK{RESET}")
        print(f"{AZUL}{NEGRITA}══════════════════════════════════════{RESET}")
        print(f"  {CIAN}1.{RESET} Cargar un auto nuevo")
        print(f"  {CIAN}2.{RESET} Ver listado de autos")
        print(f"  {CIAN}3.{RESET} Buscar un auto")
        print(f"  {CIAN}4.{RESET} Cambiar estado de un auto")
        print(f"  {CIAN}5.{RESET} Dar de baja un auto")
        print(f"  {GRIS}9. Volver al menú principal{RESET}")
        print(f"{AZUL}══════════════════════════════════════{RESET}")
        opcion = input(f"{BLANCO}¿Qué querés hacer? {RESET}").strip()

        if opcion == "1":
            cargar_auto()
        elif opcion == "2":
            listar_autos()
        elif opcion == "3":
            buscar_auto()
        elif opcion == "4":
            cambiar_estado_auto()
        elif opcion == "5":
            dar_de_baja_auto()
        elif opcion == "9":
            break
        else:
            aviso("Opción inválida, intentá de nuevo.")


# ──────────────────────────────────────────────
#  CARGAR
# ──────────────────────────────────────────────

def cargar_auto():
    global contador_id_autos
    print(f"\n{NEGRITA}── Cargar auto nuevo ──{RESET}")

    patente = input("Patente: ").strip().upper()
    if _patente_existe(patente):
        error("Ya existe un auto con esa patente.")
        return

    marca  = input("Marca: ").strip()
    modelo = input("Modelo: ").strip()

    anio = _pedir_entero("Año: ")
    if anio is None:
        return

    km = _pedir_entero("Kilómetros: ")
    if km is None:
        return

    precio = _pedir_entero("Precio de venta: ")
    if precio is None:
        return

    auto = {
        "id": contador_id_autos,
        "patente": patente,
        "marca": marca,
        "modelo": modelo,
        "anio": anio,
        "kilometros": km,
        "precio": precio,
        "estado": "disponible",
        "fecha_ingreso": date.today(),
    }

    autos.append(auto)
    contador_id_autos += 1
    guardar_en_json()  # Guarda después de agregar
    ok(f"Auto #{auto['id']} cargado correctamente.")


# ──────────────────────────────────────────────
#  LISTAR (con filtros)
# ──────────────────────────────────────────────

def listar_autos():
    if not autos:
        info("No hay autos cargados.")
        return

    print(f"\n{NEGRITA}── Filtros (Enter para saltear) ──{RESET}")
    marca_filtro  = input("Filtrar por marca: ").strip().lower()
    estado_filtro = input("Filtrar por estado (disponible/reservado/vendido/en taller): ").strip().lower()
    precio_min    = _pedir_entero_opcional("Precio mínimo: ")
    precio_max    = _pedir_entero_opcional("Precio máximo: ")

    resultado = _aplicar_filtros(marca_filtro, estado_filtro, precio_min, precio_max)

    if not resultado:
        info("No se encontraron autos con esos filtros.")
        return

    encabezado = f"{'ID':<5} {'Patente':<10} {'Marca':<12} {'Modelo':<16} {'Año':<6} {'Km':<8} {'Precio':<12} {'Estado':<12} {'Ingreso'}"
    print(f"\n{NEGRITA}{AZUL}{encabezado}{RESET}")
    print(f"{AZUL}{'─' * 90}{RESET}")
    for a in resultado:
        color_estado = _color_estado(a["estado"])
        print(
            f"{GRIS}{a['id']:<5}{RESET} {a['patente']:<10} {a['marca']:<12} {a['modelo']:<16} "
            f"{a['anio']:<6} {a['kilometros']:<8} {VERDE}${a['precio']:<11}{RESET} "
            f"{color_estado}{a['estado']:<12}{RESET} {a['fecha_ingreso']}"
        )


def _color_estado(estado):
    colores = {
        "disponible": VERDE,
        "reservado":  AMARILLO,
        "vendido":    CIAN + NEGRITA,
        "en taller":  ROJO,
    }
    return colores.get(estado, RESET)


def _aplicar_filtros(marca, estado, precio_min, precio_max):
    resultado = []
    for a in autos:
        if marca and marca not in a["marca"].lower():
            continue
        if estado and a["estado"] != estado:
            continue
        if precio_min is not None and a["precio"] < precio_min:
            continue
        if precio_max is not None and a["precio"] > precio_max:
            continue
        resultado.append(a)
    return resultado


# ──────────────────────────────────────────────
#  BUSCAR
# ──────────────────────────────────────────────

def buscar_auto():
    print(f"\n{NEGRITA}── Buscar auto ──{RESET}")
    print(f"  {CIAN}1.{RESET} Por patente")
    print(f"  {CIAN}2.{RESET} Por número interno")
    criterio = input("Elegí: ").strip()

    if criterio == "1":
        patente = input("Patente: ").strip().upper()
        auto = _buscar_por_patente(patente)
    elif criterio == "2":
        id_auto = _pedir_entero("Número interno: ")
        auto = _buscar_por_id(id_auto) if id_auto is not None else None
    else:
        aviso("Opción inválida.")
        return

    if auto:
        _mostrar_auto_detalle(auto)
    else:
        info("No se encontró ningún auto.")


def _mostrar_auto_detalle(auto):
    print(f"\n{NEGRITA}{AZUL}── Detalle del auto ──{RESET}")
    for clave, valor in auto.items():
        print(f"  {CIAN}{clave}:{RESET} {valor}")


# ──────────────────────────────────────────────
#  CAMBIAR ESTADO
# ──────────────────────────────────────────────

def cambiar_estado_auto():
    print(f"\n{NEGRITA}── Cambiar estado ──{RESET}")
    id_auto = _pedir_entero("Número interno del auto: ")
    auto = _buscar_por_id(id_auto) if id_auto is not None else None

    if not auto:
        info("Auto no encontrado.")
        return

    color = _color_estado(auto["estado"])
    print(f"  Estado actual: {color}{auto['estado']}{RESET}")
    print(f"  Estados posibles: {CIAN}{', '.join(ESTADOS_VALIDOS)}{RESET}")
    nuevo_estado = input("Nuevo estado: ").strip().lower()

    if nuevo_estado not in ESTADOS_VALIDOS:
        error("Estado inválido.")
        return

    auto["estado"] = nuevo_estado
    guardar_en_json()  # Guarda después de modificar
    ok(f"Estado actualizado a '{nuevo_estado}'.")


# ──────────────────────────────────────────────
#  DAR DE BAJA
# ──────────────────────────────────────────────

def dar_de_baja_auto():
    print(f"\n{NEGRITA}── Dar de baja un auto ──{RESET}")
    id_auto = _pedir_entero("Número interno del auto: ")
    auto = _buscar_por_id(id_auto) if id_auto is not None else None

    if not auto:
        info("Auto no encontrado.")
        return

    _mostrar_auto_detalle(auto)
    confirmacion = input(f"\n{AMARILLO}¿Confirmás la baja? (s/n): {RESET}").strip().lower()

    if confirmacion == "s":
        autos.remove(auto)
        guardar_en_json()  # Guarda después de borrar
        ok("Auto dado de baja correctamente.")
    else:
        print(f"{GRIS}↩️  Operación cancelada.{RESET}")


# ──────────────────────────────────────────────
#  HELPERS INTERNOS
# ──────────────────────────────────────────────

def _buscar_por_id(id_auto):
    for a in autos:
        if a["id"] == id_auto:
            return a
    return None


def _buscar_por_patente(patente):
    for a in autos:
        if a["patente"] == patente:
            return a
    return None


def _patente_existe(patente):
    return _buscar_por_patente(patente) is not None


def _pedir_entero(mensaje):
    try:
        return int(input(mensaje).strip())
    except ValueError:
        error("Tiene que ser un número entero.")
        return None


def _pedir_entero_opcional(mensaje):
    valor = input(mensaje).strip()
    if valor == "":
        return None
    try:
        return int(valor)
    except ValueError:
        aviso("Valor ignorado (no era un número).")
        return None