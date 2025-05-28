
import requests
import json

# Función para obtener coordenadas desde una ciudad
def get_coordinates(city, api_key):
    url = f"https://graphhopper.com/api/1/geocode?q={city}&limit=1&key={api_key}"
    response = requests.get(url)
    data = response.json()
    try:
        lat = data['hits'][0]['point']['lat']
        lon = data['hits'][0]['point']['lng']
        return lat, lon
    except:
        print(f"❌ No se encontraron coordenadas para: {city}")
        return None, None

# Función para obtener información de la ruta entre dos coordenadas
def get_route_info(from_coords, to_coords, api_key):
    url = f"https://graphhopper.com/api/1/route"
    params = {
        "point": [f"{from_coords[0]},{from_coords[1]}", f"{to_coords[0]},{to_coords[1]}"],
        "vehicle": "car",
        "locale": "es",
        "instructions": "true",
        "calc_points": "true",
        "key": api_key
    }
    response = requests.get(url, params=params)
    return response.json()

# Función principal que une todo
def main():
    api_key = "075a70d4-5801-47db-8c01-758f33a9afec"  

    while True:
        origen = input("📍 Ciudad de Origen (o 'q' para salir): ")
        if origen.lower() in ['q', 'quit']:
            print("🔚 Saliendo del programa...")
            break

        destino = input("🏁 Ciudad de Destino: ")
        if destino.lower() in ['q', 'quit']:
            print("🔚 Saliendo del programa...")
            break

        orig_coords = get_coordinates(origen, api_key)
        dest_coords = get_coordinates(destino, api_key)

        if None in orig_coords or None in dest_coords:
            continue

        data = get_route_info(orig_coords, dest_coords, api_key)

        try:
            path = data['paths'][0]
            distance_km = round(path['distance'] / 1000, 2)
            time_sec = path['time'] / 1000
            hours = int(time_sec // 3600)
            minutes = int((time_sec % 3600) // 60)
            seconds = int(time_sec % 60)
            fuel_liters = round(distance_km * 0.12, 2)  # Aproximación de 12L cada 100km

            print(f"\n📏 Distancia: {distance_km:.2f} km")
            print(f"🕒 Duración: {hours}h {minutes}m {seconds}s")
            print(f"⛽ Combustible estimado: {fuel_liters:.2f} litros")

            print("\n📝 Indicaciones del viaje:")
            for instr in path['instructions']:
                print(f" - {instr['text']} ({round(instr['distance'], 2)} m)")

            print("\n✅ Ruta consultada exitosamente\n")

        except Exception as e:
            print("❌ Error procesando los datos:", e)

# Ejecutar el programa
if __name__ == "__main__":
    main()
