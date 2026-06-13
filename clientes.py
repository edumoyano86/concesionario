import json
from rich.console import Console
from rich.table import Table

console = Console()



class clientes: 
    def __init__(persona, id_interno, dni, nombre, telefono, email, localidad, busqueda):
        persona.id_interno = id_interno
        persona.dni = dni
        persona.nombre = nombre
        persona.telefono = telefono
        persona.email = email
        persona.localidad = localidad
        persona.busqueda = busqueda
        persona.auto_comprados = []   
        persona.reservas_activas = []

    def __str__(persona):
        auto = ", ".join(persona.auto_comprados) if persona.auto_comprados else "ninguno"
        reservas = ", ".join(persona.reservas_activas) if persona.reservas_activas else "ninguno"
        return (
            f"\n[bold green]-- Cliente Encontrado --[/bold green]\n"
            f"ID: {persona.id_interno} | DNI: {persona.dni} | Nombre: {persona.nombre}\n"
            f"Contacto: {persona.telefono} / {persona.email} | Localidad: {persona.localidad}\n"
            f"Interés: {persona.busqueda}\n"
            f"Compras: {auto} | Reservas: {reservas}\n"
            f"---------------------------------------------------------------"
        )

    def to_dict(persona):
        return {
            "id_interno": persona.id_interno,
            "dni": persona.dni,
            "nombre": persona.nombre,
            "telefono": persona.telefono,
            "email": persona.email,
            "localidad": persona.localidad,
            "busqueda": persona.busqueda,
            "auto_comprados": persona.auto_comprados,
            "reservas_activas": persona.reservas_activas
        }


class GestionClientes:
    def __init__(sistema, archivo_json="concesionario.json"): # ACA REALICE UN CAMBIO EN EL NOMBRE DEL ARCHIVO JSON
        sistema.base_datos = {}
        sistema.proximo_id = 1 
        sistema.archivo_json = archivo_json
        sistema.cargar_desde_json()

    def registrar(sistema, dni, nombre, telefono, email, localidad, busqueda):
        nuevo = clientes(sistema.proximo_id, dni, nombre, telefono, email, localidad, busqueda)
        sistema.base_datos[sistema.proximo_id] = nuevo
        sistema.proximo_id += 1
        sistema.guardar_en_json()

    def lista_de_clientes(sistema):
        if not sistema.base_datos:
            console.print("[bold red]No hay clientes registrados en la base de datos.[/bold red]")
            return
        tabla = Table(title="[bold cyan]LISTADO DE CLIENTES[/bold cyan]", border_style="cyan")
        
        tabla.add_column("ID", justify="center", style="cyan")
        tabla.add_column("DNI", style="white")
        tabla.add_column("Nombre", style="white")
        tabla.add_column("Teléfono", style="white")
        tabla.add_column("Correo", style="white")
        tabla.add_column("Localidad", style="white")
        tabla.add_column("Búsqueda / Interés", style="white")
        tabla.add_column("Compras", style="white")
        tabla.add_column("Reservas", style="white")

        for cliente in sistema.base_datos.values():
            autos_str = ", ".join(cliente.auto_comprados) if cliente.auto_comprados else "ninguno"
            reservas_str = ", ".join(cliente.reservas_activas) if cliente.reservas_activas else "ninguno"

            tabla.add_row(
                str(cliente.id_interno),
                cliente.dni,
                cliente.nombre,
                cliente.telefono,
                cliente.email,
                cliente.localidad,
                cliente.busqueda,
                autos_str,
                reservas_str
            )
        console.print(tabla)   

    def buscar(sistema, dato):
        clientes_encontrados = [cliente for cliente in sistema.base_datos.values()
                               if dato == cliente.dni or dato.lower() in cliente.nombre.lower()]
        if clientes_encontrados:
            for c in clientes_encontrados: 
                console.print(c)
        else: 
            console.print(f"[yellow]No se encontró nada para: {dato}[/yellow]")

    def actualizar_contacto(sistema, id_interno, nuevo_telefono=None, nuevo_email=None, nueva_busqueda=None):
        cliente = sistema.base_datos.get(id_interno)
        if not cliente:
            console.print(f"\n[bold red]No se encontró ningún cliente con el ID {id_interno}.[/bold red]")
            return False
        
        if nuevo_telefono:
            cliente.telefono = nuevo_telefono
        if nuevo_email:
            cliente.email = nuevo_email
        if nueva_busqueda:
            cliente.busqueda = nueva_busqueda
            
        sistema.guardar_en_json()
        console.print(f"\n[bold green]Datos actualizados del cliente ID {id_interno}![/bold green]")
        return True

    def borrar(sistema, id_interno): 
        if id_interno in sistema.base_datos:
            eliminado = sistema.base_datos.pop(id_interno)
            sistema.guardar_en_json()
            console.print(f"[bold green]Se eliminó a {eliminado.nombre} del sistema.[/bold green]")
        else: 
            console.print("[bold red]ID no encontrado.[/bold red]")

    def guardar_en_json(sistema):
        datos_comunes = {}
        for id_int, cliente in sistema.base_datos.items():
            datos_comunes[id_int] = cliente.to_dict()
        with open(sistema.archivo_json, "w", encoding="utf-8") as archivo:
            json.dump(datos_comunes, archivo, indent=4, ensure_ascii=False)

    def cargar_desde_json(sistema):
        try:
            with open(sistema.archivo_json, "r", encoding="utf-8") as archivo:
                datos_cargados = json.load(archivo)
                # ACA MODIFIQUE PARA QUE SOLO LEA LOS DATOS QUE PERTENECEN A CLIENTES Y NO TRAIGA 
                datos_clientes = datos_cargados.get("clientes", {})
                for id_str, datos in datos_clientes.items():
                    id_int = int(id_str)
                    nuevo_cliente = clientes(
                        datos["id_interno"], datos["dni"], datos["nombre"],
                        datos["telefono"], datos["email"], datos["localidad"], datos["busqueda"]
                    )
                    nuevo_cliente.auto_comprados = datos["auto_comprados"]
                    nuevo_cliente.reservas_activas = datos["reservas_activas"]
                    sistema.base_datos[id_int] = nuevo_cliente

                if sistema.base_datos:
                    sistema.proximo_id = max(sistema.base_datos.keys()) + 1
        except FileNotFoundError:
            pass 


# ACA METI TODO EL MENU EN UNA FUNCION PARA QUE LO PUEDA LLAMAR DESDE MAIN
def menu_clientes():
    mi_concesionaria = GestionClientes() 

    while True:
        console.print("\n[bold magenta]=== SISTEMA DE GESTIÓN DE CLIENTES ===[/bold magenta]")
        console.print("[cyan]1.[/cyan] Registrar nuevo cliente")
        console.print("[cyan]2.[/cyan] Mostrar listado de clientes")
        console.print("[cyan]3.[/cyan] Buscar cliente por Nombre o DNI ")
        console.print("[cyan]4.[/cyan] Actualizar datos de contacto")
        console.print("[cyan]5.[/cyan] Agregar Compra / Reserva")
        console.print("[cyan]6.[/cyan] Eliminar cliente")
        console.print("[cyan]7.[/cyan] Salir")
    
        opcion = input("\nSeleccione una opción (1-7): ").strip()

        if opcion == "1":
            console.print("\n[bold yellow]--- Registrar Nuevo Cliente ---[/bold yellow]")
            dni = input("DNI: ").strip()
            nombre = input("Nombre completo: ").strip()
            telefono = input("Teléfono: ").strip()
            email = input("Email: ").strip()
            localidad = input("Localidad: ").strip()
            busqueda = input("Vehículo de interés: ").strip()
            
            if dni and nombre:
                mi_concesionaria.registrar(dni, nombre, telefono, email, localidad, busqueda)
                console.print("[bold green]¡Cliente registrado con éxito![/bold green]")
            else:
                console.print("[bold red]Error: El DNI y el Nombre son obligatorios.[/bold red]")

        elif opcion == "2":
            console.print("")
            mi_concesionaria.lista_de_clientes()

        elif opcion == "3":
            console.print("\n[bold yellow]--- Buscar Cliente ---[/bold yellow]")
            dato = input("Ingrese el Nombre o DNI a buscar: ").strip()
            if dato:
                mi_concesionaria.buscar(dato)
            else:
                console.print("[bold red]Debe ingresar un término de búsqueda.[/bold red]")

        elif opcion == "4":
            console.print("\n[bold yellow]--- Actualizar Contacto ---[/bold yellow]")
            try:
                id_int = int(input("Ingrese el ID del cliente a modificar: "))
                if id_int in mi_concesionaria.base_datos:
                    console.print("[italic gray]Deje en blanco (Enter) lo que NO desee modificar.[/italic gray]")
                    tel = input("Nuevo Teléfono: ").strip() or None
                    email = input("Nuevo Email: ").strip() or None
                    busq = input("Nueva Búsqueda: ").strip() or None
                
                    mi_concesionaria.actualizar_contacto(id_int, nuevo_telefono=tel, nuevo_email=email, nueva_busqueda=busq)
                else:
                    console.print("[bold red]El ID ingresado no corresponde a ningún cliente.[/bold red]")
            except ValueError:
                console.print("[bold red]Error: El ID debe ser un número entero.[/bold red]")

        elif opcion == "5":
            console.print("\n[bold yellow]--- Agregar Compra o Reserva ---[/bold yellow]")
            try:
                id_int = int(input("Ingrese el ID del cliente: "))
                cliente = mi_concesionaria.base_datos.get(id_int)
                if cliente:
                    console.print("[cyan]1.[/cyan] Agregar Vehículo Comprado")
                    console.print("[cyan]2.[/cyan] Agregar Reserva Activa")
                    sub_opcion = input("Seleccione (1-2): ").strip()
                
                    if sub_opcion == "1":
                        auto = input("Ingrese el modelo del auto comprado: ").strip()
                        if auto: 
                            cliente.auto_comprados.append(auto)
                            mi_concesionaria.guardar_en_json()
                            console.print(f"[bold green]¡'{auto}' agregado a compras de {cliente.nombre}![/bold green]")
                    elif sub_opcion == "2":
                        reserva = input("Ingrese el modelo del auto reservado: ").strip()
                        if reserva: 
                            cliente.reservas_activas.append(reserva)
                            mi_concesionaria.guardar_en_json()
                            console.print(f"[bold green]¡'{reserva}' agregado a reservas de {cliente.nombre}![/bold green]")
                else:
                    console.print("[bold red]El ID ingresado no existe.[/bold red]")
            except ValueError:
                console.print("[bold red]Error: El ID debe ser un número entero.[/bold red]")

        elif opcion == "6":
            console.print("\n[bold yellow]--- Eliminar Cliente ---[/bold yellow]")
            try:
                id_int = int(input("Ingrese el ID del cliente a dar de baja: "))
                if id_int in mi_concesionaria.base_datos:
                    confirmacion = input(f"¿Seguro que desea eliminar al ID {id_int}? (s/n): ").strip().lower()
                    if confirmacion == 's':
                        mi_concesionaria.borrar(id_int)
                    else:
                        console.print("[yellow]Operación cancelada.[/yellow]")
                else:
                    console.print("[bold red]El ID ingresado no existe.[/bold red]")
            except ValueError:
                console.print("[bold red]Error: El ID debe ser un número entero.[/bold red]")

        elif opcion == "7":
            console.print("\n[bold green]¡Cambios guardados correctamente! Saliendo del sistema...[/bold green]\n")
            break
        else:
            console.print("[bold red]Opción inválida. Intente de nuevo con un número del 1 al 7.[/bold red]")
# ESTO TAMBIN LO PUSE POR LO MISMO DE METER TODO DENTRO DE LA FUNCION 
if __name__ == "__main__":
    menu_clientes() 