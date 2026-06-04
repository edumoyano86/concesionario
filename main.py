# main.py
import os
import ventas
from colores import *

def limpiar_pantalla():
    """Limpia la terminal de forma nativa en cualquier sistema operativo"""
    os.system('clear' if os.name != 'nt' else 'cls')

def iniciar_sistema_menu():
    while True:
        limpiar_pantalla()

        ancho = 50
        
        # 1. Dibujamos el separador superior (usando multiplicación de strings)
        print(f"{DIM}{CYAN}{'═' * ancho}{RESET}")
        
        # 2. Títulos en Rojo y Azul con sus respectivos RESETs directos
        print(f"{BOLD}{ROJO_B}{'🚗  AUTOS DEL LITORAL  🚗':^{ancho}}{RESET}")
        print(f"{BOLD}{AZUL_B}{'SISTEMA DE GESTIÓN':^{ancho}}{RESET}")
        
        # 3. Separador medio
        print(f"{DIM}{CYAN}{'═' * ancho}{RESET}")
        print()
        
        # 4. Opciones del menú con estilos y colores directos en las cadenas
        print(f"  {CYAN}[1]{RESET} {BLANCO_B}Módulo Autos       {RESET}{DIM}──  🚗 Stock y vehículos{RESET}")
        print(f"  {CYAN}[2]{RESET} {BLANCO_B}Módulo Clientes    {RESET}{DIM}──  👥 Base de clientes{RESET}")
        print(f"  {CYAN}[3]{RESET} {BLANCO_B}Módulo Ventas      {RESET}{DIM}──  💰 Registrar operaciones{RESET}")
        print()
        
        # 5. Opción salir
        print(f"  {ROJO_B}[0] {DIM}Salir del Programa{RESET}")
        print()
        
        # 6. Separador inferior
        print(f"{DIM}{CYAN}{'─' * ancho}{RESET}")

        opc = input(f"\n{CYAN_B}  ▶  Seleccione una opción: {RESET}").strip()

        match opc:
            case "1":
                limpiar_pantalla()
                print(f"{AZUL_B}🔹 Módulo de Autos — En desarrollo{RESET}")
                print()
                input(f"{DIM}  Presione Enter para volver...{RESET}")
            case "2":
                limpiar_pantalla()
                print(f"{AZUL_B}🔹 Módulo de Clientes — En desarrollo{RESET}")
                print()
                input(f"{DIM}  Presione Enter para volver...{RESET}")
            case "3":
                limpiar_pantalla()
                print(f"{VERDE_B}✅ Redireccionando al área de ventas...{RESET}")
                ventas.mostrar_menu_ventas()
            case "0":
                limpiar_pantalla()
                print()
                print(f"{AMARILLO_B}  👋  ¡Muchas gracias por usar el sistema!{RESET}")
                print(f"{DIM}  Hasta pronto.{RESET}")
                print()
                break
            case _:
                print()
                print(f"{AMARILLO_B}⚠  Opción no válida. Por favor, intente de nuevo.{RESET}")
                input(f"{DIM}  Presione Enter para continuar...{RESET}")

if __name__ == "__main__":
    iniciar_sistema_menu()