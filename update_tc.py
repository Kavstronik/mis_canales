import requests
import json
import re
import sys

def get_tc_link():
    video_id = "x7wijay"
    # Atacamos la API de metadatos que usa el reproductor móvil
    api_url = f"https://www.dailymotion.com/player/metadata/video/{video_id}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
        "Referer": "https://www.tctelevision.com/",
        "Origin": "https://www.tctelevision.com",
        "X-Forwarded-For": "186.101.0.1" # Simula una IP de Ecuador
    }

    try:
        print(f"📡 Solicitando acceso de dispositivo móvil para TC...")
        # Usamos una sesión para mantener cookies de 'paso'
        session = requests.Session()
        # Primero 'tocamos' la web oficial para que nos den una cookie de sesión
        session.get("https://www.tctelevision.com/envivo", headers=headers, timeout=10)
        
        # Ahora pedimos el link del video con esa sesión
        response = session.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # Buscamos el stream 'auto' que es el que vimos en tu captura de red
            stream_url = data.get('qualities', {}).get('auto', [{}])[0].get('url')
            
            if stream_url:
                print("✅ ¡Bypass regional exitoso! Link capturado.")
                return stream_url
        
        print(f"⚠️ El servidor respondió con status {response.status_code}. El bloqueo persiste.")
            
    except Exception as e:
        print(f"❌ Error técnico en la infiltración: {e}")
    
    return None

# --- Lógica de actualización del JSON ---
archivo_json = 'canales.json'

try:
    nuevo_link = get_tc_link()
    if not nuevo_link:
        sys.exit(1)

    with open(archivo_json, 'r', encoding='utf-8') as f:
        canales = json.load(f)

    for c in canales:
        if "TC" in c.get('nombre', '').upper():
            c['url'] = nuevo_link
            print(f"🚀 Link de TC actualizado en el JSON.")
            break
            
    with open(archivo_json, 'w', encoding='utf-8') as f:
        json.dump(canales, f, indent=2, ensure_ascii=False)
        
except Exception as e:
    print(f"❌ Fallo al procesar el archivo local: {e}")
    sys.exit(1)
