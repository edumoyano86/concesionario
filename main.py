import os
from autos import menu_autos
import clientes
import ventas
from rich.console import Console

console = Console(color_system="standard")

def limpiar_pantalla():
    os.system('clear' if os.name != 'nt' else 'cls')

def aviso(msg): console.print(f"[yellow]⚠️  {msg}[/]")

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
        console.print(f"  [cyan][3][/] Registrar operación  [bright_black]──  💰 Ventas y reservas[/]")
        console.print()
        console.print(f"  [red][9] [bright_black]Salir del Programa[/]")
        console.print()
        console.print(f"[bright_black]{'─' * ancho}[/]")

        opc = console.input(f"\n[white]  ▶  Seleccione una opción: [/]").strip()

        match opc:
            case "1":
                menu_autos()
            case "2":
                clientes.menu_clientes()
                console.input("[bright_black]  Presione Enter para volver...[/]")
            case "3":
                ventas.mostrar_menu_ventas()
                console.input("[bright_black]  Presione Enter para volver...[/]")
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
