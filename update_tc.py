import requests
import re
import json
import sys

def get_tc_link():
    # URL de la página donde TC tiene su reproductor
    url_web = "https://www.tctelevision.com/envivo"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url_web, headers=headers, timeout=15)
        # Buscamos directamente la cadena que contiene el token 'sec='
        # TC suele usar el ID x7wijay de Dailymotion
        match = re.search(r'sec=([a-zA-Z0-9_-]+)', response.text)
        
        if match:
            token = match.group(1)
            print(f"✅ Token atrapado: {token[:15]}...")
            return f"https://cdndirector.dailymotion.com/cdn/live/video/x7wijay.m3u8?sec={token}"
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    return None

archivo_json = 'canales.json'

try:
    with open(archivo_json, 'r', encoding='utf-8') as f:
        lista_canales = json.load(f)

    nuevo_link = get_tc_link()
    
    if not nuevo_link:
        print("❌ ERROR: No se encontró el token 'sec=' en el código de la web.")
        sys.exit(1)

    actualizado = False
    for canal in lista_canales:
        # Buscamos "TC" en el nombre (sin importar tildes o mayúsculas)
        if "TC" in canal.get('nombre', '').upper():
            if canal['url'] != nuevo_link:
                canal['url'] = nuevo_link
                actualizado = True
                print(f"✅ URL de TC actualizada en el objeto JSON.")
            else:
                print("ℹ️ El link en el JSON ya es el mismo que el de la web.")
            break
    
    if actualizado:
        with open(archivo_json, 'w', encoding='utf-8') as f:
            json.dump(lista_canales, f, indent=2, ensure_ascii=False)
        print("🚀 ¡CAMBIO GUARDADO EN EL ARCHIVO!")
    else:
        print("ℹ️ No se requirieron cambios físicos en el archivo.")

except Exception as e:
    print(f"❌ Fallo crítico: {e}")
    sys.exit(1)
