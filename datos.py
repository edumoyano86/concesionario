import json
import os

def cargar_todo():
    estructura_principal = {
        "autos": [],       
        "clientes": [],    
        "ventas": [],      
        "vendedores": [],
        "reservas": []   
    }

    if os.path.exists("data/autos.json"):
        try:
            with open("data/autos.json", "r", encoding="utf-8") as f:
                contenido = json.load(f)
                if isinstance(contenido, dict) and "autos" in contenido:
                    estructura_principal["autos"] = contenido["autos"]
                else:
                    estructura_principal["autos"] = contenido
        except Exception:
            estructura_principal["autos"] = []

    if os.path.exists("data/clientes.json"):
        try:
            with open("data/clientes.json", "r", encoding="utf-8") as f:
                estructura_principal["clientes"] = json.load(f)
        except Exception:
            estructura_principal["clientes"] = []
    
    if os.path.exists("data/ventas.json"):
        try:
            with open("data/ventas.json", "r", encoding="utf-8") as f:
                estructura_principal["ventas"] = json.load(f)
        except Exception:
            estructura_principal["ventas"] = []

    if os.path.exists("data/vendedores.json"):
        try:
            with open("data/vendedores.json", "r", encoding="utf-8") as f:
                estructura_principal["vendedores"] = json.load(f)
        except Exception:
            estructura_principal["vendedores"] = []

    if os.path.exists("data/reservas.json"):
        try:
            with open("data/reservas.json", "r", encoding="utf-8") as f:
                estructura_principal["reservas"] = json.load(f)
        except Exception:
            estructura_principal["reservas"] = []
    
    return estructura_principal

def guardar_todo(datos_generales):
    
    with open("data/autos.json", "w") as f:
        json.dump(datos_generales["autos"], f, indent=4)
    
    with open("data/clientes.json", "w") as f:
        json.dump(datos_generales["clientes"], f, indent=4)
        
    with open("data/ventas.json", "w") as f:
        json.dump(datos_generales["ventas"], f, indent=4)
        
    with open("data/vendedores.json", "w") as f:
        json.dump(datos_generales["vendedores"], f, indent=4)
    
    with open("data/reservas.json", "w") as f:
        json.dump(datos_generales["reservas"], f, indent=4)