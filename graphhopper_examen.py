import requests
import json
print(" \n")
print("Programa de cálculo de distancia usando GraphHopper (Examen DevNet)\n")

from datetime import datetime
key = "ba17bd7b-191c-43b8-ba6a-08ad54de386a"
geo_url = "https://graphhopper.com/api/1/geocode"

while True:
    print("\nPara salir, presione la tecla 'v'")
    origen = input("Ingrese la ciudad de origen: ")
    if origen.lower() == "v":
        print("Saliendo del programa...")
        break
    destino = input("Ingrese la ciudad de destino: ")
    if destino.lower() == "v":
        print("Saliendo del programa...")
        break
    print("\nMedios de transporte disponibles: car, bike, foot")
    transporte = input("Ingrese el medio de transporte: ")
    if transporte.lower() == "v":
        print("Saliendo del programa...")
        break

    # Coordenadas de origen
    params_loc1 = {
        "q": origen,
        "locale": "es",
        "limit": 1,
        "key": key
    }
    resp_loc1 = requests.get(geo_url, params=params_loc1)
    data_loc1 = resp_loc1.json()
    lat_loc1 = data_loc1["hits"][0]["point"]["lat"]
    lon_loc1 = data_loc1["hits"][0]["point"]["lng"]

    # Coordenadas de destino
    params_loc2 = {
        "q": destino,
        "locale": "es",
        "limit": 1,
        "key": key
    }

    resp_loc2 = requests.get(geo_url, params=params_loc2)
    data_loc2 = resp_loc2.json()
    lat_loc2 = data_loc2["hits"][0]["point"]["lat"]
    lon_loc2 = data_loc2["hits"][0]["point"]["lng"]

    # Cálculo de distancia y tiempo usando API GraphHopper
    route_url = f"https://graphhopper.com/api/1/route?key={key}"
    body = {
        "profile": transporte,
        "points": [
            [lon_loc1, lat_loc1],
            [lon_loc2, lat_loc2]
        ],
        "locale": "es",
        "instructions": True
    }

    resp_route = requests.post(route_url, json=body)
    data_route = resp_route.json()

    distancia_m = data_route["paths"][0]["distance"]
    tiempo_ms = data_route["paths"][0]["time"]
    instrucciones = data_route["paths"][0]["instructions"]

    distancia_km = distancia_m / 1000
    distancia_millas = distancia_km * 0.621371
    tiempo_horas = tiempo_ms / 3600000

    # Fecha y hora de la consulta 
    fecha_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    print("\nResultados del cálculo")
    print(f"Distancia: {distancia_km:.2f} km")
    print(f"Distancia: {distancia_millas:.2f} millas")
    print(f"Duración estimada: {tiempo_horas:.2f} horas")
    print("\nNarrativa del viaje")
    for paso in instrucciones:
        print(f"- {paso['text']}")
    print("\nCálculo finalizado.\n")
    print("\nFecha y hora de la consulta") 
    print(fecha_hora)
    print("\nRealizado por Raimundo Lisboa\n")
