
import json
import os
from datetime import date
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

ARCHIVO_JSON = "concesionario.json"


# Funciones para el manejo del JSON 

def cargar_datos():
    with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    
    for v in datos.get("ventas", []):
        if isinstance(v.get("fecha_venta"), str):
            v["fecha_venta"] = date.fromisoformat(v["fecha_venta"])
            
    return datos


def guardar_datos(datos):
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False, default=str)


# Menu principal de ventas

def mostrar_menu_ventas():
    while True:
        datos = cargar_datos()

        console.print("\n")
        menu_texto = (
            "[bold cyan][1][/bold cyan] Registrar una venta nueva\n"
            "[bold cyan][2][/bold cyan] Ver todas las ventas hechas\n"
            "[bold cyan][3][/bold cyan] Buscar una venta\n"
            "[bold cyan][4][/bold cyan] Modificar el estado del pago\n"
            "[bold cyan][5][/bold cyan] Eliminar / Anular una venta\n\n"
            "[bold yellow][9][/bold yellow] Volver al Menú Principal"
        )
        console.print(Panel(menu_texto, title="💰 ÁREA DE VENTAS", border_style="cyan", width=50))

        opcion_sel = input("▶ Seleccione una opción: ").strip()

        if not opcion_sel:
            continue

        match opcion_sel:
            case "1":
                registrar_venta(datos)
                guardar_datos(datos)
            case "2":
                listar_ventas(datos)
            case "3":
                buscar_venta(datos)
            case "4":
                modificar_estado_pago(datos)
                guardar_datos(datos)
            case "5":
                eliminar_venta(datos)
                guardar_datos(datos)
            case "9":
                console.print("\n[bold green]✅ Volviendo al menú principal...[/bold green]")
                break
            case _:
                console.print("\n[bold red]⚠ Opción inválida. Intente de nuevo.[/bold red]")


# Para registrar una venta

def registrar_venta(datos):
    lista_ventas = datos.get("ventas", [])
    lista_autos = datos.get("autos", [])
    lista_clientes = datos.get("clientes", [])
    lista_vendedores = datos.get("vendedores", [])

    console.print("\n─── REGISTRAR NUEVA VENTA ───", style="bold blue")

    id_auto_str = input("▶ ID del auto a vender: ").strip()
    if not id_auto_str.isdigit():
        console.print("[bold red]❌ El ID debe ser un número entero.[/bold red]")
        return
    id_auto = int(id_auto_str)

    auto_encontrado = None
    for auto in lista_autos:
        if auto["id"] == id_auto:
            auto_encontrado = auto
            break

    if not auto_encontrado:
        console.print("[bold red]❌ El ID de auto no existe en el sistema.[/bold red]")
        return

    if auto_encontrado.get("estado") == "vendido":
        console.print("[bold red]❌ Este auto ya fue vendido previamente.[/bold red]")
        return

    id_cliente_str = input("▶ ID del cliente comprador: ").strip()
    if not id_cliente_str.isdigit():
        console.print("[bold red]❌ El ID debe ser un número entero.[/bold red]")
        return
    id_cliente = int(id_cliente_str)

    cliente_existe = False
    for c in lista_clientes:
        if c["id"] == id_cliente:
            cliente_existe = True
            break
            
    if not cliente_existe:
        console.print("[bold red]❌ El ID de cliente no está registrado.[/bold red]")
        return

    id_vendedor_str = input("▶ ID del vendedor: ").strip()
    if not id_vendedor_str.isdigit():
        console.print("[bold red]❌ El ID debe ser un número entero.[/bold red]")
        return
    id_vendedor = int(id_vendedor_str)

    vendedor_existe = False
    for v in lista_vendedores:
        if v["id"] == id_vendedor:
            vendedor_existe = True
            break

    if not vendedor_existe:
        console.print("[bold red]❌ El ID de vendedor no existe en el sistema.[/bold red]")
        return

    precio_str = input(f"▶ Precio final acordado (Precio lista ${auto_encontrado.get('precio', 0)}): ").strip()
    if not precio_str.isdigit():
        console.print("[bold red]❌ El precio debe ser un número entero.[/bold red]")
        return
    precio_final = int(precio_str)

    forma_pago = input("▶ Forma de pago (contado / financiado / parte de pago): ").strip().lower()
    estado_pago = input("▶ Estado del pago (cobrado / pendiente / en cuotas): ").strip().lower()

    auto_encontrado["estado"] = "vendido"

    nuevo_id = 1
    for v in lista_ventas:
        if v["id"] >= nuevo_id:
            nuevo_id = v["id"] + 1


    nueva_venta = {
        "id": nuevo_id,
        "id_auto": id_auto,
        "id_cliente": id_cliente,
        "id_vendedor": id_vendedor,
        "fecha_venta": date.today(),
        "precio_final": precio_final,
        "forma_pago": forma_pago,
        "estado_pago": estado_pago
    }

    lista_ventas.append(nueva_venta)
    console.print(f"\n[bold green]✅ ¡Venta #{nuevo_id} registrada con éxito! El auto pasó automáticamente a 'vendido'.[/bold green]")


# Muestra todas las ventas hechas

def listar_ventas(datos):
    lista_ventas = datos.get("ventas", [])

    if not lista_ventas:
        console.print("\n[bold yellow]⚠ No hay ventas registradas en el sistema todavía.[/bold yellow]")
        return

    table = Table(title="📋 HISTORIAL DE VENTAS HECHAS", title_style="bold blue")
    table.add_column("ID Venta", justify="center", style="cyan")
    table.add_column("ID Auto", justify="center")
    table.add_column("ID Cliente", justify="center")
    table.add_column("ID Vend.", justify="center")
    table.add_column("Fecha", justify="center", style="magenta")
    table.add_column("Precio Final", justify="right", style="green")
    table.add_column("Forma Pago", justify="center")
    table.add_column("Estado Pago", justify="center", style="yellow")

    for v in lista_ventas:
        fecha_str = v["fecha_venta"].strftime("%Y-%m-%d") if isinstance(v["fecha_venta"], date) else str(v["fecha_venta"])
        
        table.add_row(
            str(v["id"]),
            str(v["id_auto"]),
            str(v["id_cliente"]),
            str(v["id_vendedor"]),
            fecha_str,
            f"${v['precio_final']}",
            v["forma_pago"],
            v["estado_pago"]
        )

    console.print(table)


# Busqueda de ventas por patente, DNI o ID
def buscar_venta(datos):
    lista_ventas = datos.get("ventas", [])

    console.print("\n[bold cyan]Opciones de búsqueda:[/bold cyan]")
    print(" [1] Buscar por Patente del auto")
    print(" [2] Buscar por DNI del cliente")
    print(" [3] Buscar por ID de Vendedor")
    
    criterio = input("\n▶ Seleccione opción de búsqueda: ").strip()
    encontrado = False

    match criterio:
        case "1":
            patente_buscar = input("Ingrese la patente del auto: ").strip().upper()
            id_auto_encontrado = None
            for auto in datos.get("autos", []):
                if auto["patente"].upper() == patente_buscar:
                    id_auto_encontrado = auto["id"]
                    break
            
            if id_auto_encontrado is not None:
                for v in lista_ventas:
                    if v["id_auto"] == id_auto_encontrado:
                        _imprimir_detalle_venta(v)
                        encontrado = True
                        
        case "2":
            dni_buscar = input("Ingrese el DNI del cliente: ").strip()
            id_cliente_encontrado = None
            for cliente in datos.get("clientes", []):
                if cliente["dni"] == dni_buscar:
                    id_cliente_encontrado = cliente["id"]
                    break
                    
            if id_cliente_encontrado is not None:
                for v in lista_ventas:
                    if v["id_cliente"] == id_cliente_encontrado:
                        _imprimir_detalle_venta(v)
                        encontrado = True
                        
        case "3":
            id_vendedor_str = input("Ingrese el ID del Vendedor: ").strip()
            if id_vendedor_str.isdigit():
                id_buscar = int(id_vendedor_str)
                for v in lista_ventas:
                    if v["id_vendedor"] == id_buscar:
                        _imprimir_detalle_venta(v)
                        encontrado = True
        case _:
            console.print("[bold red]❌ Opción de búsqueda inválida.[/bold red]")
            return

    if not encontrado:
        console.print("[bold red]❌ No se encontró ninguna venta con ese criterio.[/bold red]")


def _imprimir_detalle_venta(v):
    fecha_str = v["fecha_venta"].strftime("%Y-%m-%d") if isinstance(v["fecha_venta"], date) else str(v["fecha_venta"])
    detalle = (
        f"🚗 [bold]Auto (ID):[/bold] {v['id_auto']}\n"
        f"👤 [bold]Cliente (ID):[/bold] {v['id_cliente']}\n"
        f"🧑‍💼 [bold]Vendedor (ID):[/bold] {v['id_vendedor']}\n"
        f"📅 [bold]Fecha:[/bold] {fecha_str}\n"
        f"💰 [bold]Monto final:[/bold] [green]${v['precio_final']}[/green]\n"
        f"💳 [bold]Forma / Estado:[/bold] {v['forma_pago']} ({v['estado_pago']})"
    )
    console.print(Panel(detalle, title=f"🟢 Venta Encontrada #{v['id']}", border_style="green", width=45))


# Para modificar el estado de pago si se vendio en cuotas

def modificar_estado_pago(datos):
    lista_ventas = datos.get("ventas", [])
    
    id_str = input("▶ Ingrese el ID de la venta a modificar: ").strip()
    if not id_str.isdigit():
        consoleprint("[bold red]❌ El ID debe ser un número.[/bold red]")
        return
    id_buscar = int(id_str)

    for v in lista_ventas:
        if v["id"] == id_buscar:
            console.print(f"Venta encontrada. Estado de pago actual: [yellow]{v['estado_pago']}[/yellow]")
            nuevo_estado = input("▶ Ingrese nuevo estado (cobrado / pendiente / en cuotas): ").strip().lower()
            if nuevo_estado:
                v["estado_pago"] = nuevo_estado
                console.print("[bold green]✅ Estado de pago actualizado con éxito.[/bold green]")
            return

    console.print("[bold red]❌ No se encontró ninguna venta con ese ID.[/bold red]")

# Para eliminar una Venta

def eliminar_venta(datos):
    lista_ventas = datos.get("ventas", [])
    lista_autos = datos.get("autos", [])

    id_str = input("▶ Ingrese el ID de la venta que desea ANULAR: ").strip()
    if not id_str.isdigit():
        console.print("[bold red]❌ El ID debe ser un número.[/bold red]")
        return
    id_buscar = int(id_str)

    for v in lista_ventas:
        if v["id"] == id_buscar:
            confirmar = input(f"⚠ ¿Está seguro de anular la venta #{v['id']}? (S/N): ").strip().upper()
            if confirmar == "S":
                for auto in lista_autos:
                    if auto["id"] == v["id_auto"]:
                        auto["estado"] = "disponible"
                        break
                
                lista_ventas.remove(v)
                console.print("[bold green]✅ Venta eliminada. El auto vuelve a estar 'disponible' en el stock.[/bold green]")
                return
            else:
                console.print("[bold blue]🔹 Operación cancelada. No se modificaron datos.[/bold blue]")
                return

    console.print("[bold red]❌ No se encontró ninguna venta con ese ID.[/bold red]")


# Ejecución standalone para pruebas
if __name__ == "__main__":
    mostrar_menu_ventas()