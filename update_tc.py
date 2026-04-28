import requests
import re
import json

def get_tc_link():
    url_web = "https://www.tctelevision.com/envivo"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        response = requests.get(url_web, headers=headers)
        # Buscamos el token sec que genera Dailymotion en la web de TC
        match = re.search(r'x7wijay\?sec=([a-zA-Z0-9_-]+)', response.text)
        if match:
            token = match.group(1)
            # Retornamos el link completo con el nuevo token
            return f"https://cdndirector.dailymotion.com/cdn/live/video/x7wijay.m3u8?sec={token}"
    except Exception as e:
        print(f"Error al obtener el link: {e}")
    return None

# Abrir y leer tu JSON (formato lista directa)
archivo_json = 'mis_canales.json' # Asegúrate que se llame así en tu repo
with open(archivo_json, 'r', encoding='utf-8') as f:
    lista_canales = json.load(f)

# Buscar TC Televisión y actualizar la URL
nuevo_link = get_tc_link()
if nuevo_link:
    for canal in lista_canales:
        if canal['nombre'] == "TC Televisión":
            canal['url'] = nuevo_link
            print(f"URL de TC actualizada correctamente.")

# Guardar los cambios con el formato original
with open(archivo_json, 'w', encoding='utf-8') as f:
    json.dump(lista_canales, f, indent=2, ensure_ascii=False)
