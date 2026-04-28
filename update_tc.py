import requests
import re
import json

def get_tc_link():
    url_web = "https://www.tctelevision.com/envivo"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        response = requests.get(url_web, headers=headers, timeout=10)
        # Buscamos el token sec (esto es lo que cambia diario)
        match = re.search(r'x7wijay\?sec=([a-zA-Z0-9_-]+)', response.text)
        if match:
            token = match.group(1)
            # El link limpio sin los parámetros basura de dmTs que también caducan
            return f"https://cdndirector.dailymotion.com/cdn/live/video/x7wijay.m3u8?sec={token}"
    except Exception as e:
        print(f"Error en la petición: {e}")
    return None

archivo_json = 'canales.json'

try:
    with open(archivo_json, 'r', encoding='utf-8') as f:
        lista_canales = json.load(f)

    nuevo_link = get_tc_link()

    if nuevo_link:
        encontrado = False
        for canal in lista_canales:
            # USAMOS .upper() para que no importe si es minúscula o mayúscula
            # Y buscamos solo la palabra "TC" para evitar líos con la tilde
            nombre_canal = canal.get('nombre', '').upper()
            if "TC" in nombre_canal:
                canal['url'] = nuevo_link
                encontrado = True
                print(f"✅ ¡ÉXITO! Se actualizó TC con el link: {nuevo_link}")
                break
        
        if not encontrado:
            print("⚠️ ERROR: No se encontró ningún canal que contenga 'TC' en el JSON.")
        
        # Solo guardamos si hubo cambios
        if encontrado:
            with open(archivo_json, 'w', encoding='utf-8') as f:
                json.dump(lista_canales, f, indent=2, ensure_ascii=False)
    else:
        print("⚠️ ERROR: No se pudo obtener el link nuevo de la web de TC.")

except Exception as e:
    print(f"Fallo crítico: {e}")
