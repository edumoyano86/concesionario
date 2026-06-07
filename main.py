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

    def __init__(sistema, archivo_json="clientes.json"):
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
            console.print("[bold red]No Hay Clientes Registrados en la Base de Datos[/bold red]")
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
            console.print(f"No se encontró nada para: {dato}")

    def actualizar_contacto(sistema, id_interno, nuevo_telefono=None, nuevo_email=None, nueva_busqueda=None):
        cliente = sistema.base_datos.get(id_interno)
        if not cliente:
            console.print(f"\n No se encontro ningun cliente con el id {id_interno}.")
            return False
        
        if nuevo_telefono:
            cliente.telefono = nuevo_telefono
        if nuevo_email:
            cliente.email = nuevo_email
        if nueva_busqueda:
            cliente.busqueda = nueva_busqueda
            
        sistema.guardar_en_json()
        console.print(f"\n Datos actualizados del cliente {id_interno}")
        return True

    def borrar(sistema, id_interno): 
        if id_interno in sistema.base_datos:
            eliminado = sistema.base_datos.pop(id_interno)
            sistema.guardar_en_json()
            console.print(f"Se elimino a {eliminado.nombre} del sistema.")
        else: 
            console.print("ID no encontrado.")

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
                for id_str, datos in datos_cargados.items():
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
mi_concesionaria = GestionClientes()

mi_concesionaria.registrar("44.644.133", "Milton Conforti", "3447468035", "Miltonconfortii@gmail.com", "San Jose", "Volkswagen polo")
mi_concesionaria.registrar("23.018.591", "Marisel Lopez","1165439432", "marisegl@gmail.com", "Colon", "Vehiculo 3 puertas" )
cliente_milton = mi_concesionaria.base_datos.get(1)
if cliente_milton:
    cliente_milton.auto_comprados.append("Polo Gts 2023")
    cliente_milton.reservas_activas.append("VW Golf gti 2016")

console.print("\n---.LISTA ACTUAL.---")
mi_concesionaria.lista_de_clientes()

console.print("\n--- BUSCANDO A 'CONFORTI' ---")
mi_concesionaria.buscar("Conforti")

console.print("\n --- ACTUALIZANDO A MARISEL (ID: 2) ---")
mi_concesionaria.actualizar_contacto(id_interno=2, nuevo_telefono="3447-456754", nueva_busqueda= "camioneta ranger")

console.print("\n---LISTA DE CLIENTES ACTUALIZADA---")
mi_concesionaria.lista_de_clientes()