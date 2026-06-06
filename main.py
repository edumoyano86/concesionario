#pip install -r requirements.txt

import ventas
from rich.console import Console

console = Console(color_system="standard")

def iniciar_sistema_menu():
    while True:
        ancho = 55        
       
        console.print("[dim cyan]" + "═" * ancho + "[/dim cyan]")
        console.print(f"[bold red]{'🚗  AUTOS DEL LITORAL  🚗':^{ancho}}[/bold red]")
        console.print(f"[bold blue]{'SISTEMA DE GESTIÓN':^{ancho}}[/bold blue]")
        console.print("[dim cyan]" + "═" * ancho + "[/dim cyan]")
        console.print()
        
        console.print("  [cyan][1][/cyan] [bold white]Módulo Autos[/bold white]       [dim]──  🚗 Stock y vehículos[/dim]")
        console.print("  [cyan][2][/cyan] [bold white]Módulo Clientes[/bold white]    [dim]──  👥 Base de clientes[/dim]")
        console.print("  [cyan][3][/cyan] [bold white]Módulo Ventas[/bold white]      [dim]──  💰 Registrar operaciones[/dim]")
        console.print()
        
        console.print("  [bold red][0][/bold red] [dim]Salir del Programa[/dim]")
        console.print()
        
        console.print("[dim cyan]" + "─" * ancho + "[/dim cyan]")

        opc = input("\n  ▶  Seleccione una opción: ").strip()

        match opc:
            case "1":
                console.print("[bold blue]🔹 Módulo de Autos — En desarrollo[/bold blue]")
                console.print()
                input("  Presione Enter para volver...")
            case "2":
                console.print("[bold blue]🔹 Módulo de Clientes — En desarrollo[/bold blue]")
                console.print()
                input("  Presione Enter para volver...")
            case "3":
                console.print("[bold green]✅ Redireccionando al área de ventas...[/bold green]")
                ventas.mostrar_menu_ventas()
            case "0":
                console.print()
                console.print("  [bold yellow]👋  ¡Muchas gracias por usar el sistema![/bold yellow]")
                console.print("  [dim]Hasta pronto.[/dim]")
                console.print()
                break
            case _:
                console.print()
                console.print("  [bold yellow]⚠  Opción no válida. Por favor, intente de nuevo.[/bold yellow]")
                input("  Presione Enter para continuar...")

if __name__ == "__main__":
    iniciar_sistema_menu()