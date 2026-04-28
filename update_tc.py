import requests
import json
import sys

def get_tc_link():
    video_id = "x7wijay"
    # Paso 1: Pedir un Token de Invitado a Dailymotion
    auth_url = "https://www.dailymotion.com/player/metadata/video/" + video_id
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://www.tctelevision.com/",
        "Accept": "application/json"
    }

    try:
        print(f"🔑 Solicitando pase de invitado para TC...")
        session = requests.Session()
        # Hacemos una petición inicial para capturar cookies de sesión
        session.get("https://www.dailymotion.com/embed/video/" + video_id, headers=headers, timeout=10)
        
        # Paso 2: Usar la sesión para obtener los metadatos reales
        response = session.get(auth_url, headers=headers, timeout=10)
        data = response.json()
        
        # Buscamos la URL del stream en las diferentes calidades
        # Dailymotion lo guarda en 'qualities' -> 'auto'
        stream_url = data.get('qualities', {}).get('auto', [{}])[0].get('url')
        
        if stream_url:
            print("✅ ¡Pase aceptado! URL generada correctamente.")
            return stream_url
        else:
            print("❌ Dailymotion entregó datos vacíos. El bloqueo de IP persiste.")
            
    except Exception as e:
        print(f"❌ Error técnico: {e}")
    
    return None

# --- Lógica de actualización del archivo canales.json ---
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
            print(f"🚀 Link actualizado en el JSON.")
            break
            
    with open(archivo_json, 'w', encoding='utf-8') as f:
        json.dump(canales, f, indent=2, ensure_ascii=False)
        
except Exception as e:
    print(f"❌ Fallo al escribir el archivo: {e}")
    sys.exit(1)
