import os
from autos import menu_autos

# from clientes import menu_clientes     
# from vendedores import menu_vendedores 
# from ventas import menu_ventas         
# from reservas import menu_reservas     

VERDE    = "\033[92m"
ROJO     = "\033[91m"
AMARILLO = "\033[93m"
AZUL     = "\033[94m"
CIAN     = "\033[96m"
BLANCO   = "\033[97m"
GRIS     = "\033[90m"
RESET    = "\033[0m"
NEGRITA  = "\033[1m"

def limpiar_pantalla():
    os.system('clear' if os.name != 'nt' else 'cls')

def aviso(msg): print(f"{AMARILLO}⚠️  {msg}{RESET}")

#  SUBMENÚ: BASE DE CLIENTES

def menu_base_clientes():
    while True:
        limpiar_pantalla()
        ancho = 50
        print(f"{AZUL}{NEGRITA}{'═' * ancho}{RESET}")
        print(f"{AZUL}{NEGRITA}{'👥  BASE DE CLIENTES':^{ancho}}{RESET}")
        print(f"{AZUL}{NEGRITA}{'═' * ancho}{RESET}")
        print()
        print(f"  {CIAN}[1]{RESET} Clientes           {GRIS}──  👤 Gestión de clientes{RESET}")
        print(f"  {CIAN}[2]{RESET} Vendedores         {GRIS}──  👔 Gestión de vendedores{RESET}")
        print()
        print(f"  {GRIS}[9] Volver al menú principal{RESET}")
        print()
        print(f"{GRIS}{'─' * ancho}{RESET}")
        opc = input(f"\n{BLANCO}  ▶  Seleccione una opción: {RESET}").strip()

        match opc:
            case "1":
                limpiar_pantalla()
                print(f"{AMARILLO}⚠️  Módulo de Clientes — En desarrollo{RESET}")
                print()
                input(f"{GRIS}  Presione Enter para volver...{RESET}")
                # menu_clientes()
            case "2":
                limpiar_pantalla()
                print(f"{AMARILLO}⚠️  Módulo de Vendedores — En desarrollo{RESET}")
                print()
                input(f"{GRIS}  Presione Enter para volver...{RESET}")
                # menu_vendedores()
            case "9":
                break
            case _:
                aviso("Opción no válida. Por favor, intente de nuevo.")
                input(f"{GRIS}  Presione Enter para continuar...{RESET}")

#  SUBMENÚ: REGISTRAR OPERACIONES

def menu_operaciones():
    while True:
        limpiar_pantalla()
        ancho = 50
        print(f"{VERDE}{NEGRITA}{'═' * ancho}{RESET}")
        print(f"{VERDE}{NEGRITA}{'💰  REGISTRAR OPERACIONES':^{ancho}}{RESET}")
        print(f"{VERDE}{NEGRITA}{'═' * ancho}{RESET}")
        print()
        print(f"  {CIAN}[1]{RESET} Ventas             {GRIS}──  💵 Registrar ventas{RESET}")
        print(f"  {CIAN}[2]{RESET} Reservas           {GRIS}──  📌 Registrar reservas{RESET}")
        print()
        print(f"  {GRIS}[9] Volver al menú principal{RESET}")
        print()
        print(f"{GRIS}{'─' * ancho}{RESET}")
        opc = input(f"\n{BLANCO}  ▶  Seleccione una opción: {RESET}").strip()

        match opc:
            case "1":
                limpiar_pantalla()
                print(f"{AMARILLO}⚠️  Módulo de Ventas — En desarrollo{RESET}")
                print()
                input(f"{GRIS}  Presione Enter para volver...{RESET}")
                # menu_ventas()
            case "2":
                limpiar_pantalla()
                print(f"{AMARILLO}⚠️  Módulo de Reservas — En desarrollo{RESET}")
                print()
                input(f"{GRIS}  Presione Enter para volver...{RESET}")
                # menu_reservas()
            case "9":
                break
            case _:
                aviso("Opción no válida. Por favor, intente de nuevo.")
                input(f"{GRIS}  Presione Enter para continuar...{RESET}")

#  MENÚ PRINCIPAL

def iniciar_sistema_menu():
    while True:
        limpiar_pantalla()
        ancho = 50

        print(f"{AZUL}{NEGRITA}{'═' * ancho}{RESET}")
        print(f"{ROJO}{NEGRITA}{'🚗  AUTOS DEL LITORAL — Sistema v1.0':^{ancho}}{RESET}")
        print(f"{AZUL}{NEGRITA}{'═' * ancho}{RESET}")
        print()
        print(f"  {CIAN}[1]{RESET} Stock de vehículos {GRIS}──  🚗 Autos en stock{RESET}")
        print(f"  {CIAN}[2]{RESET} Base de clientes   {GRIS}──  👥 Clientes y vendedores{RESET}")
        print(f"  {CIAN}[3]{RESET} Registrar operac.  {GRIS}──  💰 Ventas y reservas{RESET}")
        print()
        print(f"  {ROJO}[9] {GRIS}Salir del Programa{RESET}")
        print()
        print(f"{GRIS}{'─' * ancho}{RESET}")

        opc = input(f"\n{BLANCO}  ▶  Seleccione una opción: {RESET}").strip()

        match opc:
            case "1":
                menu_autos()
            case "2":
                menu_base_clientes()
            case "3":
                menu_operaciones()
            case "9":
                limpiar_pantalla()
                print()
                print(f"{AMARILLO}  👋  ¡Muchas gracias por usar el sistema!{RESET}")
                print(f"{GRIS}  Hasta pronto.{RESET}")
                print()
                break
            case _:
                aviso("Opción no válida. Por favor, intente de nuevo.")
                input(f"{GRIS}  Presione Enter para continuar...{RESET}")

if __name__ == "__main__":
    iniciar_sistema_menu()