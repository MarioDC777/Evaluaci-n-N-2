import requests

API_KEY = "65c778b1-0a2d-4e18-bce0-d402c10d5b64"

def obtener_coordenadas(ciudad):
    url = "https://graphhopper.com/api/1/geocode"
    params = {
        "q": ciudad,
        "key": API_KEY,
        "limit": 1
    }
    respuesta = requests.get(url, params=params)
    data = respuesta.json()
    
    if not data['hits']:
        raise ValueError(f"No se encontró la ciudad: {ciudad}")
    
    lat = data['hits'][0]['point']['lat']
    lng = data['hits'][0]['point']['lng']
    return f"{lat},{lng}"

def obtener_datos(origen, destino):
    coord_origen = obtener_coordenadas(origen)
    coord_destino = obtener_coordenadas(destino)

    url = "https://graphhopper.com/api/1/route"
    params = {
        "point": [coord_origen, coord_destino],
        "vehicle": "car",
        "locale": "es",
        "calc_points": "true",
        "instructions": "true",
        "key": API_KEY
    }

    respuesta = requests.get(url, params=params)
    data = respuesta.json()

    if "paths" not in data:
        print("❌ Error en la respuesta de la API:")
        print(data)
        return

    ruta = data['paths'][0]
    distancia_km = ruta['distance'] / 1000
    duracion_segundos = ruta['time'] / 1000
    narrativa = ruta['instructions']
    combustible = distancia_km / 12  # 12 km por litro

    horas = int(duracion_segundos // 3600)
    minutos = int((duracion_segundos % 3600) // 60)
    segundos = int(duracion_segundos % 60)

    print(f"\nDistancia: {distancia_km:.2f} km")
    print(f"Duración: {horas}h {minutos}m {segundos}s")
    print(f"Combustible requerido: {combustible:.2f} litros")
    print("\nNarrativa del viaje:")
    for paso in narrativa:
        print(f"- {paso['text']}")

# Programa principal
while True:
    origen = input("Ciudad de origen (ej. Santiago): ")
    if origen.lower() == "q":
        break
    destino = input("Ciudad de destino (ej. Ovalle): ")
    if destino.lower() == "q":
        break

    try:
        obtener_datos(origen, destino)
    except Exception as e:
        print(f"⚠️ Error: {e}")

    salir = input("\nPresiona 'q' para salir o Enter para continuar: ")
    if salir.lower() == "q":
        break

