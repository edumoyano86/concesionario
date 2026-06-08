import json
from datetime import date
from rich.console import Console

console = Console(color_system="standard")

autos = []
contador_id_autos = 1

ESTADOS_VALIDOS = ("disponible", "reservado", "vendido", "en taller")
ARCHIVO_JSON    = "concesionario.json"

def ok(msg):    console.print(f"[green]✅ {msg}[/]")
def error(msg): console.print(f"[red]❌ {msg}[/]")
def aviso(msg): console.print(f"[yellow]⚠️  {msg}[/]")
def info(msg):  console.print(f"[cyan]🔍 {msg}[/]")

def _formatear_precio(valor):
    return f"${valor:,}".replace(",", ".")

def _formatear_kilometros(valor):
    return f"{valor:,}".replace(",", ".")

#   JSON

def cargar_desde_json():
    global autos, contador_id_autos
    try:
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
            datos = json.load(f)
        for a in datos["autos"]:
            a["fecha_ingreso"] = date.fromisoformat(a["fecha_ingreso"])
        autos = datos["autos"]
        if autos:
            contador_id_autos = max(a["id"] for a in autos) + 1
    except FileNotFoundError:
        autos = []
    except json.JSONDecodeError:
        aviso("El archivo JSON estaba dañado. Se arranca con lista vacía.")
        autos = []


def guardar_en_json():
    datos = {
        "autos": [],
        "clientes": [],
        "ventas": [],
        "vendedores": []
    }
    for a in autos:
        copia = a.copy()
        copia["fecha_ingreso"] = a["fecha_ingreso"].isoformat()
        datos["autos"].append(copia)
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
        
#   MENÚ

def menu_autos():
    cargar_desde_json()
    while True:
        console.print(f"\n[bold blue]══════════════════════════════════════[/]")
        console.print(f"[bold blue]  🚗 AUTOS EN STOCK[/]")
        console.print(f"[bold blue]══════════════════════════════════════[/]")
        console.print(f"  [cyan]1.[/] Cargar un auto nuevo")
        console.print(f"  [cyan]2.[/] Ver listado de autos")
        console.print(f"  [cyan]3.[/] Buscar un auto")
        console.print(f"  [cyan]4.[/] Cambiar estado de un auto")
        console.print(f"  [cyan]5.[/] Dar de baja un auto")
        console.print(f"  [bright_black]9. Volver al menú principal[/]")
        console.print(f"[blue]══════════════════════════════════════[/]")
        opcion = console.input(f"[white]¿Qué querés hacer? [/]").strip()

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

#   CARGAR

def cargar_auto():
    global contador_id_autos
    console.print(f"\n[bold]── Cargar auto nuevo ──[/]")

    patente = input("Patente: ").strip().upper()
    if _patente_existe(patente):
        error("Ya existe un auto con esa patente.")
        return

    marca  = input("Marca: ").strip().upper()
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
    guardar_en_json()
    ok(f"Auto #{auto['id']} cargado correctamente.")

#   LISTAR (con filtros)

def listar_autos():
    if not autos:
        info("No hay autos cargados.")
        return

    console.print(f"\n[bold]── Filtros (Enter para saltear) ──[/]")
    marca_filtro  = input("Filtrar por marca: ").strip().lower()
    estado_filtro = input("Filtrar por estado (disponible/reservado/vendido/en taller): ").strip().lower()
    precio_min    = _pedir_entero_opcional("Precio mínimo: ")
    precio_max    = _pedir_entero_opcional("Precio máximo: ")

    resultado = _aplicar_filtros(marca_filtro, estado_filtro, precio_min, precio_max)

    if not resultado:
        info("No se encontraron autos con esos filtros.")
        return

    encabezado = f"{'ID':<5} {'Patente':<10} {'Marca':<12} {'Modelo':<16} {'Año':<6} {'Km':<8} {'Precio':<12} {'Estado':<12} {'Ingreso'}"
    console.print(f"\n[blue]{encabezado}[/]", soft_wrap=True)
    console.print(f"[blue]{'─' * 100}[/]", soft_wrap=True)
    for a in resultado:
        color_estado = _color_estado(a["estado"])
        console.print(
            f"[bright_white]{a['id']:<5}[/] [bright_white]{a['patente']:<10}[/] [bright_white]{a['marca']:<12}[/] [bright_white]{a['modelo']:<16}[/] "
            f"[bright_white]{a['anio']:<6}[/] [bright_white]{_formatear_kilometros(a['kilometros']):<8}[/] "
            f"[green]{_formatear_precio(a['precio']):<12}[/] "
            f"{color_estado}{a['estado'].upper():<12}[/] [bright_white]{a['fecha_ingreso']}[/]",
            soft_wrap=True,
        )


def _color_estado(estado):
    colores = {
        "disponible": "[green]",
        "reservado":  "[yellow]",
        "vendido":    "[bold green]",
        "en taller":  "[red]",
    }
    return colores.get(estado, "")


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

#   BUSCAR

def buscar_auto():
    console.print(f"\n[bold]── Buscar auto ──[/]")
    console.print(f"  [cyan]1.[/] Por patente")
    console.print(f"  [cyan]2.[/] Por número interno")
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
    etiquetas = {
        "id": "ID", "patente": "Patente", "marca": "Marca",
        "modelo": "Modelo", "anio": "Año", "kilometros": "Km",
        "precio": "Precio", "estado": "Estado", "fecha_ingreso": "Ingreso",
    }
    colores = {
        "id": "[bright_white]", "anio": "[white]",
        "kilometros": "[white]", "precio": "[green]", "fecha_ingreso": "[white]",
    }
    console.print(f"\n[bold blue]── Detalle del auto ──[/]")
    for clave, valor in auto.items():
        etiqueta = etiquetas.get(clave, clave)
        if clave == "precio":
            valor = _formatear_precio(valor)
        elif clave in ("marca", "estado"):
            valor = valor.upper()
        color = colores.get(clave, "")
        if clave == "estado":
            color = _color_estado(valor.lower() if isinstance(valor, str) else "disponible")
        if color:
            console.print(f"  [cyan]{etiqueta}:[/] {color}{valor}[/]")
        else:
            console.print(f"  [cyan]{etiqueta}:[/] {valor}")

#   CAMBIAR ESTADO

def cambiar_estado_auto():
    console.print(f"\n[bold]── Cambiar estado ──[/]")
    id_auto = _pedir_entero("Número interno del auto: ")
    auto = _buscar_por_id(id_auto) if id_auto is not None else None

    if not auto:
        info("Auto no encontrado.")
        return

    color = _color_estado(auto["estado"])
    console.print(f"  Estado actual: {color}{auto['estado'].upper()}[/]")
    console.print(f"  Estados posibles: [cyan]{', '.join(ESTADOS_VALIDOS)}[/]")
    nuevo_estado = input("Nuevo estado: ").strip().lower()

    if nuevo_estado not in ESTADOS_VALIDOS:
        error("Estado inválido.")
        return

    auto["estado"] = nuevo_estado
    guardar_en_json()
    ok(f"Estado actualizado a '{nuevo_estado}'.")

#   DAR DE BAJA

def dar_de_baja_auto():
    console.print(f"\n[bold]── Dar de baja un auto ──[/]")
    id_auto = _pedir_entero("Número interno del auto: ")
    auto = _buscar_por_id(id_auto) if id_auto is not None else None

    if not auto:
        info("Auto no encontrado.")
        return

    _mostrar_auto_detalle(auto)
    confirmacion = console.input(f"\n[yellow]¿Confirmás la baja? (s/n): [/]").strip().lower()

    if confirmacion == "s":
        autos.remove(auto)
        guardar_en_json()
        ok("Auto dado de baja correctamente.")
    else:
        console.print("[bright_black]↩️  Operación cancelada.[/]")

#  HELPERS INTERNOS

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
