import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

# Menu

def menu_vendedores(datos_actualizados):
    while True:
        console.print("\n")
        menu_texto = (
            "[bold cyan][1][/bold cyan] Registrar un vendedor nuevo\n"
            "[bold cyan][2][/bold cyan] Ver todos los vendedores\n"
            "[bold cyan][3][/bold cyan] Modificar datos de un vendedor\n"
            "[bold cyan][4][/bold cyan] Dar de baja / alta un vendedor\n"
            "[bold cyan][5][/bold cyan] Calcular comisiones mensuales\n\n"
            "[bold yellow][9][/bold yellow] Volver al Menú Principal"
        )
        console.print(Panel(menu_texto, title="🧑‍💼 ÁREA DE VENDEDORES", border_style="cyan", width=50))

        opcion_sel = input("▶ Seleccione una opción: ").strip()

        if not opcion_sel:
            continue

        match opcion_sel:
            case "1":
                registrar_vendedor(datos_actualizados)
            case "2":
                listar_vendedores(datos_actualizados)
            case "3":
                modificar_vendedor(datos_actualizados)
            case "4":
                cambiar_estado_vendedor(datos_actualizados)
            case "5":
                calcular_comisiones(datos_actualizados)
            case "9":
                console.print("\n[bold green]✅ Volviendo al menú principal...[/bold green]")
                break
            case _:
                console.print("\n[bold red]⚠ Opción inválida. Intente de nuevo.[/bold red]")

# Funcion para registrar vendedores
def registrar_vendedor(datos_actualizados):
    lista_vendedores = datos_actualizados.get("vendedores", [])
    
    console.print("\n─── REGISTRAR NUEVO VENDEDOR ───", style="bold blue")
    
    nombre = input("▶ Nombre completo del vendedor: ").strip()
    if not nombre:
        console.print("[bold red]❌ El nombre no puede estar vacío.[/bold red]")
        return

    comision_str = input("▶ Porcentaje de comisión (ej: 3): ").strip()
    if not comision_str.isdigit():
        console.print("[bold red]❌ El porcentaje debe ser un número entero.[/bold red]")
        return
    comision = int(comision_str)

    nuevo_id = 1
    for v in lista_vendedores:
        if v["id"] >= nuevo_id:
            nuevo_id = v["id"] + 1

    nuevo_vendedor = {
        "id": nuevo_id,
        "nombre_completo": nombre,
        "comision_porcentaje": comision,
        "estado": "activo"
    }

    lista_vendedores.append(nuevo_vendedor)
    console.print(f"\n[bold green]✅ ¡Vendedor #{nuevo_id} '{nombre}' registrado con éxito![/bold green]")


# Funcion para ver todos los vendedores
def listar_vendedores(datos_actualizados):
    lista_vendedores = datos_actualizados.get("vendedores", [])

    if not lista_vendedores:
        console.print("\n[bold yellow]⚠ No hay vendedores registrados en el sistema todavía.[/bold yellow]")
        return

    tabla = Table(title="📋 NÓMINA DE VENDEDORES", title_style="bold blue")
    tabla.add_column("ID", justify="center", style="cyan")
    tabla.add_column("Nombre Completo")
    tabla.add_column("Comisión", justify="center", style="green")
    tabla.add_column("Estado", justify="center")

    for vendedor in lista_vendedores:
        estado_style = "bold green" if vendedor["estado"] == "activo" else "bold red"
        tabla.add_row(
            str(vendedor["id"]),
            vendedor["nombre_completo"],
            f"{vendedor['comision_porcentaje']}%",
            f"[{estado_style}]{vendedor['estado'].upper()}[/]"
        )

    console.print(tabla)


# Funcion para modificar datos de vendedores
def modificar_vendedor(datos_actualizados):
    listar_vendedores(datos_actualizados)  
    lista_vendedores = datos_actualizados.get("vendedores", [])

    id_str = input("\n▶ Ingrese el ID del vendedor a modificar: ").strip()
    if not id_str.isdigit():
        console.print("[bold red]❌ El ID debe ser un número entero.[/bold red]")
        return
    id_buscar = int(id_str)

    for v in lista_vendedores:
        if v["id"] == id_buscar:
            console.print(f"Vendedor encontrado: [cyan]{v['nombre_completo']}[/cyan]")
            
            nuevo_nombre = input(f"▶ Nuevo nombre (Enter para dejar '{v['nombre_completo']}'): ").strip()
            nueva_comision = input(f"▶ Nueva comisión (Enter para dejar {v['comision_porcentaje']}%): ").strip()

            if nuevo_nombre:
                v["nombre_completo"] = nuevo_nombre
            if nueva_comision:
                if nueva_comision.isdigit():
                    v["comision_porcentaje"] = int(nueva_comision)
                else:
                    console.print("[bold yellow]⚠ Comisión inválida. Se mantuvo el valor anterior.[/bold yellow]")

            console.print("[bold green]✅ Datos del vendedor actualizados con éxito.[/bold green]")
            return

    console.print("[bold red]❌ No se encontró ningún vendedor con ese ID.[/bold red]")


# Funcion para cambiar el estado de un vendedor
def cambiar_estado_vendedor(datos_actualizados):
    listar_vendedores(datos_actualizados)
    lista_vendedores = datos_actualizados.get("vendedores", [])

    id_str = input("\n▶ Ingrese el ID del vendedor para cambiar su estado (Baja/Alta): ").strip()
    if not id_str.isdigit():
        console.print("[bold red]❌ El ID debe ser un número entero.[/bold red]")
        return
    id_buscar = int(id_str)

    for vendedor in lista_vendedores:
        if vendedor["id"] == id_buscar:
            nuevo_estado = "inactivo" if vendedor["estado"] == "activo" else "active"
            vendedor["estado"] = "inactivo" if vendedor["estado"] == "activo" else "activo"
            console.print(f"[bold green]✅ El vendedor ahora está: {vendedor['estado'].upper()}[/bold green]")
            return

    console.print("[bold red]❌ No se encontró ningún vendedor con ese ID.[/bold red]")


# Funcion para calcular comisiones de vendedores
def calcular_comisiones(datos_actualizados):
    lista_vendedores = datos_actualizados.get("vendedores", [])
    lista_ventas = datos_actualizados.get("ventas", [])

    if not lista_vendedores:
        console.print("\n[bold yellow]⚠ No hay vendedores registrados para calcular comisiones.[/bold yellow]")
        return

    tabla_comisiones = Table(title="💰 LIQUIDACIÓN DE COMISIONES SOBRE VENTAS", title_style="bold yellow")
    tabla_comisiones.add_column("ID Vend.", justify="center", style="cyan")
    tabla_comisiones.add_column("Vendedor")
    tabla_comisiones.add_column("Cant. Ventas", justify="center")
    tabla_comisiones.add_column("Total Facturado", justify="right", style="green")
    tabla_comisiones.add_column("Comisión Total", justify="right", style="bold green")

    for vendedor in lista_vendedores:
        ventas_totales = 0
        monto_total_vendido = 0
        
        for venta in lista_ventas:
            if venta["id_vendedor"] == vendedor["id"]:
                ventas_totales += 1
                monto_total_vendido += venta["precio_final"]

        comision_calculada = int(monto_total_vendido * (vendedor["comision_porcentaje"] / 100))

        tabla_comisiones.add_row(
            str(vendedor["id"]),
            vendedor["nombre_completo"],
            str(ventas_totales),
            f"${monto_total_vendido}",
            f"${comision_calculada}"
        )

    console.print("\n")
    console.print(tabla_comisiones)

if __name__ == "__main__":
    calcular_comisiones()
    