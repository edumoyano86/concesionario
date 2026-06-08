import os
from autos import menu_autos
from rich.console import Console

console = Console(color_system="standard")

# from clientes import menu_clientes
# from vendedores import menu_vendedores
# from ventas import menu_ventas
# from reservas import menu_reservas

def limpiar_pantalla():
    os.system('clear' if os.name != 'nt' else 'cls')

def aviso(msg): console.print(f"[yellow]⚠️  {msg}[/]")

#  SUBMENÚ: BASE DE CLIENTES

def menu_base_clientes():
    while True:
        limpiar_pantalla()
        ancho = 50
        console.print(f"[bold blue]{'═' * ancho}[/]")
        console.print(f"[bold blue]{'👥  BASE DE CLIENTES':^{ancho}}[/]")
        console.print(f"[bold blue]{'═' * ancho}[/]")
        console.print()
        console.print(f"  [cyan][1][/] Clientes           [bright_black]──  👤 Gestión de clientes[/]")
        console.print(f"  [cyan][2][/] Vendedores         [bright_black]──  👔 Gestión de vendedores[/]")
        console.print()
        console.print(f"  [bright_black][9] Volver al menú principal[/]")
        console.print()
        console.print(f"[bright_black]{'─' * ancho}[/]")
        opc = console.input(f"\n[white]  ▶  Seleccione una opción: [/]").strip()

        match opc:
            case "1":
                limpiar_pantalla()
                console.print("[yellow]⚠️  Módulo de Clientes — En desarrollo[/]")
                console.print()
                console.input("[bright_black]  Presione Enter para volver...[/]")
                # menu_clientes()
            case "2":
                limpiar_pantalla()
                console.print("[yellow]⚠️  Módulo de Vendedores — En desarrollo[/]")
                console.print()
                console.input("[bright_black]  Presione Enter para volver...[/]")
                # menu_vendedores()
            case "9":
                break
            case _:
                aviso("Opción no válida. Por favor, intente de nuevo.")
                console.input("[bright_black]  Presione Enter para continuar...[/]")

#  SUBMENÚ: REGISTRAR OPERACIONES

def menu_operaciones():
    while True:
        limpiar_pantalla()
        ancho = 50
        console.print(f"[bold green]{'═' * ancho}[/]")
        console.print(f"[bold green]{'💰  REGISTRAR OPERACIONES':^{ancho}}[/]")
        console.print(f"[bold green]{'═' * ancho}[/]")
        console.print()
        console.print(f"  [cyan][1][/] Ventas             [bright_black]──  💵 Registrar ventas[/]")
        console.print(f"  [cyan][2][/] Reservas           [bright_black]──  📌 Registrar reservas[/]")
        console.print()
        console.print(f"  [bright_black][9] Volver al menú principal[/]")
        console.print()
        console.print(f"[bright_black]{'─' * ancho}[/]")
        opc = console.input(f"\n[white]  ▶  Seleccione una opción: [/]").strip()

        match opc:
            case "1":
                limpiar_pantalla()
                console.print("[yellow]⚠️  Módulo de Ventas — En desarrollo[/]")
                console.print()
                console.input("[bright_black]  Presione Enter para volver...[/]")
                # menu_ventas()
            case "2":
                limpiar_pantalla()
                console.print("[yellow]⚠️  Módulo de Reservas — En desarrollo[/]")
                console.print()
                console.input("[bright_black]  Presione Enter para volver...[/]")
                # menu_reservas()
            case "9":
                break
            case _:
                aviso("Opción no válida. Por favor, intente de nuevo.")
                console.input("[bright_black]  Presione Enter para continuar...[/]")

#  MENÚ PRINCIPAL

def iniciar_sistema_menu():
    while True:
        limpiar_pantalla()
        ancho = 50

        console.print(f"[bold blue]{'═' * ancho}[/]")
        console.print(f"[bold red]{'🚗  AUTOS DEL LITORAL — Sistema v1.0':^{ancho}}[/]")
        console.print(f"[bold blue]{'═' * ancho}[/]")
        console.print()
        console.print(f"  [cyan][1][/] Stock de vehículos [bright_black]──  🚗 Autos en stock[/]")
        console.print(f"  [cyan][2][/] Base de clientes   [bright_black]──  👥 Clientes y vendedores[/]")
        console.print(f"  [cyan][3][/] Registrar operac.  [bright_black]──  💰 Ventas y reservas[/]")
        console.print()
        console.print(f"  [red][9] [bright_black]Salir del Programa[/]")
        console.print()
        console.print(f"[bright_black]{'─' * ancho}[/]")

        opc = console.input(f"\n[white]  ▶  Seleccione una opción: [/]").strip()

        match opc:
            case "1":
                menu_autos()
            case "2":
                menu_base_clientes()
            case "3":
                menu_operaciones()
            case "9":
                limpiar_pantalla()
                console.print()
                console.print("[yellow]  👋  ¡Muchas gracias por usar el sistema![/]")
                console.print("[bright_black]  Hasta pronto.[/]")
                console.print()
                break
            case _:
                aviso("Opción no válida. Por favor, intente de nuevo.")
                console.input("[bright_black]  Presione Enter para continuar...[/]")

if __name__ == "__main__":
    try:
        iniciar_sistema_menu()
    except KeyboardInterrupt:
        limpiar_pantalla()
        console.print()
        console.print("[yellow]  👋  ¡Muchas gracias por usar el sistema![/]")
        console.print("[bright_black]  Hasta pronto.[/]")
        console.print()
