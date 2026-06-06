
from rich.console import Console

console = Console()

from rich.table import Table


class clientes: 
    def __init__(persona,id_interno,dni,nombre,telefono,email,localidad,busqueda):
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
         f"---Cliente:{persona.nombre} (ID: {persona.id_interno})---\n"
         f"Dni: {persona.dni} | Localidad: {persona.localidad}\n"
         f"Contacto:{persona.telefono} / {persona.email}\n"
         f"interes: {persona.busqueda}\n"
         f"compras:{auto}| reservas:{reservas}\n"
         f"---------------------------------------------------------------"
 )

class GestionClientes:
    def __init__(sistema):
        sistema.base_datos = {}
        sistema.proximo_id = 1 
 
    def registrar(sistema, dni, nombre, telefono, email, localidad, busqueda):
        nuevo = clientes(sistema.proximo_id, dni, nombre, telefono, email, localidad, busqueda)
        sistema.base_datos[sistema.proximo_id] = nuevo
        sistema.proximo_id += 1
    def lista_de_clientes(sistema):
        if not sistema.base_datos:
            console.print("No Hay Clientes Registrados")
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
            for clientes in clientes_encontrados: console.print(clientes)
        else: 
            console.print(f"No se encontró nada para: {dato}")
    def actualizar_contacto(sistema, id_interno, nuevo_telefono=None, nuevo_email=None, nueva_busqueda=None):
        clientes = sistema.base_datos.get(id_interno)
        if not clientes:
            console.print(f"\n No se encontro ningun cliente con el id {id_interno}.")
            return False
        
        if nuevo_telefono:
            clientes.telefono = nuevo_telefono
        
        if nuevo_email:
            clientes.email = nuevo_email
        
        if nueva_busqueda:
            clientes.busqueda = nueva_busqueda
        console.print(f"\n Datos actualizados del cliente {id_interno}")
        return True

    def borrar(sistema, id_interno): 
        if id_interno in sistema.base_datos:
           eliminado = sistema.base_datos.pop(id_interno)
           
           console.print(f"Se elimino a {eliminado.nombre} del sistema.")
           
        else: 
            console.print("ID no encontrado.")

mi_concecionaria = GestionClientes()

mi_concecionaria.registrar("44.644.133", "Milton Conforti", "3447468035", "Miltonconfortii@gmail.com", "San Jose", "Volkswagen polo")
mi_concecionaria.registrar("23.018.591", "Marisel Lopez","1165439432", "marisegl@gmail.com", "Colon", "Vehiculo 3 puertas" )

cliente_milton = mi_concecionaria.base_datos.get(1)
if cliente_milton:
    cliente_milton.auto_comprados.append("Polo Gts 2023")
    cliente_milton.reservas_activas.append("VW Golf gti 2016")

console.print("\n---.LISTA ACTUAL.---")
mi_concecionaria.lista_de_clientes()

console.print("\n--- BUSCANDO A 'CONFORTI' ---")
mi_concecionaria.buscar("Conforti")

console.print("\n --- ACTUALIZANDO A MARISEL (ID: 2) ---")
mi_concecionaria.actualizar_contacto(id_interno=2, nuevo_telefono="3447-456754", nueva_busqueda= "camioneta ranger")

console.print("\n---LISTA DE CLIENTES ACTUALIZADA---")
mi_concecionaria.lista_de_clientes()