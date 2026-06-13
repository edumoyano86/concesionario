
import json
import os
from datetime import date
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

ARCHIVO_JSON = "concesionario.json"

# Manejo de datos del .json 

def cargar_datos():
    if not os.path.exists(ARCHIVO_JSON):
        return {"autos": [], "clientes": {}, "vendedores": [], "ventas": []}

    with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
        datos_json = json.load(archivo)
    
    for venta in datos_json.get("ventas", []):
        venta["fecha_venta"] = date.fromisoformat(venta["fecha_venta"])
            
    return datos_json


def guardar_datos(datos_json):
    ventas_guardar = []
    for venta in datos_json.get("ventas", []):
        venta_clonada = venta.copy()
        venta_clonada["fecha_venta"] = str(venta["fecha_venta"])
        ventas_guardar.append(venta_clonada)

    datos_para_disco = datos_json.copy()
    datos_para_disco["ventas"] = ventas_guardar

    with open(ARCHIVO_JSON, "w", encoding="utf-8") as archivo:
        json.dump(datos_para_disco, archivo, indent=4, ensure_ascii=False)


# Menu principal del modulo de ventas.

def menu_ventas():
    while True:
        datos_actualizados = cargar_datos()

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
                registrar_venta(datos_actualizados)
                guardar_datos(datos_actualizados)
            case "2":
                listar_ventas(datos_actualizados)
            case "3":
                buscar_venta(datos_actualizados)
            case "4":
                modificar_estado_pago(datos_actualizados)
                guardar_datos(datos_actualizados)
            case "5":
                eliminar_venta(datos_actualizados)
                guardar_datos(datos_actualizados)
            case "9":
                console.print("\n[bold green]✅ Volviendo al menú principal...[/bold green]")
                break
            case _:
                console.print("\n[bold red]⚠ Opción inválida. Intente de nuevo.[/bold red]")


# Funcion para registrar una venta nueva.

def registrar_venta(datos_actualizados):
    lista_ventas = datos_actualizados.get("ventas", [])
    lista_autos = datos_actualizados.get("autos", [])
    dic_clientes = datos_actualizados.get("clientes", {})
    lista_vendedores = datos_actualizados.get("vendedores", [])

    console.print("\n─── REGISTRAR NUEVA VENTA ───", style="bold blue")

    if not lista_autos:
        console.print("[bold yellow]⚠ No hay autos cargados en el sistema.[/bold yellow]")
        return
    
    tabla_autos = Table(title="🚗 AUTOS DISPONIBLES EN STOCK", title_style="bold green")
    tabla_autos.add_column("ID", justify="center", style="cyan")
    tabla_autos.add_column("Patente", justify="center")
    tabla_autos.add_column("Marca/Modelo")
    tabla_autos.add_column("Precio", justify="right", style="green")
    tabla_autos.add_column("Estado", justify="center")
    
    autos_disponibles = 0
    for auto in lista_autos:
        if auto.get("estado") == "disponible":
            autos_disponibles = autos_disponibles + 1
            tabla_autos.add_row(
                str(auto["id"]),
                auto["patente"],
                f"{auto['marca']} {auto['modelo']}",
                f"${auto['precio']}",
                auto["estado"]
            )
    
    if autos_disponibles == 0:
        console.print("[bold yellow]⚠ No hay autos con estado 'disponible' para vender.[/bold yellow]")
        return
        
    console.print(tabla_autos)

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

    if auto_encontrado == None:
        console.print("[bold red]❌ El ID de auto no existe en el sistema.[/bold red]")
        return

    if auto_encontrado.get("estado") == "vendido":
        console.print("[bold red]❌ Este auto ya fue vendido previamente.[/bold red]")
        return

    if not dic_clientes:
        console.print("[bold yellow]⚠ No hay clientes registrados en el sistema todavía.[/bold yellow]")
        return

    tabla_clientes = Table(title="👤 CLIENTES REGISTRADOS", title_style="bold magenta")
    tabla_clientes.add_column("ID", justify="center", style="cyan")
    tabla_clientes.add_column("DNI", justify="center")
    tabla_clientes.add_column("Nombre Completo")    
    tabla_clientes.add_column("Localidad")

    for cliente in dic_clientes.values():
        tabla_clientes.add_row(
            str(cliente["id_interno"]),
            cliente["dni"], 
            cliente["nombre"], 
            cliente["localidad"]
        )
        
    console.print("\n")
    console.print(tabla_clientes)

    id_cliente_str = input("▶ ID del cliente comprador: ").strip()
    if not id_cliente_str.isdigit():
        console.print("[bold red]❌ El ID debe ser un número entero.[/bold red]")
        return
    id_cliente = int(id_cliente_str)

    clientes_encontrados = 0
    for id_str in dic_clientes.keys():
        if int(id_str) == id_cliente:
            clientes_encontrados = 1
            break
            
    if clientes_encontrados == 0:
        console.print("[bold red]❌ El ID de cliente no está registrado.[/bold red]")
        return

    if not lista_vendedores:
        console.print("[bold yellow]⚠ No hay vendedores registrados en el sistema.[/bold yellow]")
        return

    tabla_vendedores = Table(title="🧑‍💼 VENDEDORES ACTIVOS", title_style="bold cyan")
    tabla_vendedores.add_column("ID", justify="center", style="cyan")
    tabla_vendedores.add_column("Nombre Vendedor")
    tabla_vendedores.add_column("Comisión", justify="center")

    for vendedor in lista_vendedores:
        if vendedor.get("estado") == "activo":
            tabla_vendedores.add_row(str(vendedor["id"]), vendedor["nombre_completo"], f"{vendedor['comision_porcentaje']}%")
            
    console.print("\n")
    console.print(tabla_vendedores)

    id_vendedor_str = input("▶ ID del vendedor: ").strip()
    if not id_vendedor_str.isdigit():
        console.print("[bold red]❌ El ID debe ser un número entero.[/bold red]")
        return
    id_vendedor = int(id_vendedor_str)

    vendedores_encontrados = 0
    for vendedor in lista_vendedores:
        if vendedor["id"] == id_vendedor:
            vendedores_encontrados = vendedores_encontrados + 1
            break

    if vendedores_encontrados == 0:
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

# Funcion para mostrar las ventas. 

def listar_ventas(datos_actualizados):
    lista_ventas = datos_actualizados.get("ventas", [])

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

    for venta in lista_ventas:
        fecha_str = venta["fecha_venta"].strftime("%Y-%m-%d")
        
        table.add_row(
            str(venta["id"]),
            str(venta["id_auto"]),
            str(venta["id_cliente"]),
            str(venta["id_vendedor"]),
            fecha_str,
            f"${venta['precio_final']}",
            venta["forma_pago"],
            venta["estado_pago"]
        )

    console.print(table)

# Funcion para buscar una venta.

def buscar_venta(datos_actualizados):
    lista_ventas = datos_actualizados.get("ventas", [])

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
            for auto in datos_actualizados.get("autos", []):
                if auto["patente"].upper() == patente_buscar:
                    id_auto_encontrado = auto["id"]
                    break
            
            if id_auto_encontrado is not None:
                for venta in lista_ventas:
                    if venta["id_auto"] == id_auto_encontrado:
                        imprimir_detalle_venta(venta)
                        encontrado = True
                        
        case "2":
            dni_buscar = input("Ingrese el DNI del cliente: ").strip()
            id_cliente_encontrado = None
            for cliente in datos_actualizados.get("clientes", {}).values():
                if cliente["dni"] == dni_buscar:
                    id_cliente_encontrado = cliente["id_interno"]
                    break
                    
            if id_cliente_encontrado is not None:
                for venta in lista_ventas:
                    if venta["id_cliente"] == id_cliente_encontrado:
                        imprimir_detalle_venta(venta)
                        encontrado = True
                        
        case "3":
            id_vendedor_str = input("Ingrese el ID del Vendedor: ").strip()
            if id_vendedor_str.isdigit():
                id_buscar = int(id_vendedor_str)
                for venta in lista_ventas:
                    if venta["id_vendedor"] == id_buscar:
                        imprimir_detalle_venta(venta)
                        encontrado = True
        case _:
            console.print("[bold red]❌ Opción de búsqueda inválida.[/bold red]")
            return

    if not encontrado:
        console.print("[bold red]❌ No se encontró ninguna venta con ese criterio.[/bold red]")

# Funcion para mostrar el detalle de una venta.

def imprimir_detalle_venta(venta):
    fecha_str = venta["fecha_venta"].strftime("%Y-%m-%d")
    detalle = (
        f"🚗 [bold]Auto (ID):[/bold] {venta['id_auto']}\n"
        f"👤 [bold]Cliente (ID):[/bold] {venta['id_cliente']}\n"
        f"🧑‍💼 [bold]Vendedor (ID):[/bold] {venta['id_vendedor']}\n"
        f"📅 [bold]Fecha:[/bold] {fecha_str}\n"
        f"💰 [bold]Monto final:[/bold] [green]${venta['precio_final']}[/green]\n"
        f"💳 [bold]Forma / Estado:[/bold] {venta['forma_pago']} ({venta['estado_pago']})"
    )
    console.print(Panel(detalle, title=f"🟢 Venta Encontrada #{venta['id']}", border_style="green", width=45))

# Funcion para modificar el estado de pago de una venta.

def modificar_estado_pago(datos_actualizados):
    lista_ventas = datos_actualizados.get("ventas", [])
    
    id_str = input("▶ Ingrese el ID de la venta a modificar: ").strip()
    if not id_str.isdigit():
        console.print("[bold red]❌ El ID debe ser un número.[/bold red]")
        return
    id_buscar = int(id_str)

    for venta in lista_ventas:
        if venta["id"] == id_buscar:
            console.print(f"Venta encontrada. Estado de pago actual: [yellow]{venta['estado_pago']}[/yellow]")
            nuevo_estado = input("▶ Ingrese nuevo estado (cobrado / pendiente / en cuotas): ").strip().lower()
            if nuevo_estado:
                venta["estado_pago"] = nuevo_estado
                console.print("[bold green]✅ Estado de pago actualizado con éxito.[/bold green]")
            return

    console.print("[bold red]❌ No se encontró ninguna venta con ese ID.[/bold red]")

# Funcion para eliminar una venta.

def eliminar_venta(datos_actualizados):
    lista_ventas = datos_actualizados.get("ventas", [])
    lista_autos = datos_actualizados.get("autos", [])

    id_str = input("▶ Ingrese el ID de la venta que desea ANULAR: ").strip()
    if not id_str.isdigit():
        console.print("[bold red]❌ El ID debe ser un número.[/bold red]")
        return
    id_buscar = int(id_str)

    for venta in lista_ventas:
        if venta["id"] == id_buscar:
            confirmar = input(f"⚠ ¿Está seguro de anular la venta #{venta['id']}? (S/N): ").strip().upper()
            if confirmar == "S":
                for auto in lista_autos:
                    if auto["id"] == venta["id_auto"]:
                        auto["estado"] = "disponible"
                        break
                
                lista_ventas.remove(venta)
                console.print("[bold green]✅ Venta eliminada. El auto vuelve a estar 'disponible' en el stock.[/bold green]")
                return
            else:
                console.print("[bold blue]🔹 Operación cancelada. No se modificaron datos.[/bold blue]")
                return

    console.print("[bold red]❌ No se encontró ninguna venta con ese ID.[/bold red]")


if __name__ == "__main__":
    menu_ventas()