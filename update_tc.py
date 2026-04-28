import requests
import json
import sys
import re

def get_tc_link():
    video_id = "x7wijay"
    # URL de metadatos que usa el reproductor
    api_url = f"https://www.dailymotion.com/player/metadata/video/{video_id}"
    
    # REEMPLAZA ESTO: Pega aquí el contenido de la cookie que copiaste en el Paso 1
    # Debe verse algo como "v1st=...; ts=...; "
    mi_cookie = "PEGAR_AQUI_TU_COOKIE_CAPTURADA"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://www.tctelevision.com/",
        "Cookie": mi_cookie
    }

    try:
        print(f"🕵️ Usando identidad de Guayaquil para validar sesión...")
        response = requests.get(api_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            # Buscamos el stream automático (el que vimos en tu captura de red)
            stream_url = data.get('qualities', {}).get('auto', [{}])[0].get('url')
            if stream_url:
                print("✅ ¡IDENTIDAD ACEPTADA! Link generado con éxito.")
                return stream_url
        
        print(f"❌ Error de sesión ({response.status_code}). La cookie podría estar vencida.")
    except Exception as e:
        print(f"❌ Fallo técnico: {e}")
    
    return None

# --- Lógica de actualización del JSON ---
archivo_json = 'canales.json'

nuevo_link = get_tc_link()
if nuevo_link:
    try:
        with open(archivo_json, 'r', encoding='utf-8') as f:
            canales = json.load(f)
        for c in canales:
            if "TC" in c.get('nombre', '').upper():
                c['url'] = nuevo_link
                break
        with open(archivo_json, 'w', encoding='utf-8') as f:
            json.dump(canales, f, indent=2, ensure_ascii=False)
        print("🚀 canales.json actualizado con bypass de sesión.")
    except Exception as e:
        print(f"❌ Error al guardar el archivo: {e}")
else:
    sys.exit(1)
