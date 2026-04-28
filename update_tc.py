import requests
import json
import re
import sys

def get_tc_link():
    # ID de TC Televisión en Dailymotion
    video_id = "x7wijay"
    
    # Intentamos obtener los metadatos directamente de Dailymotion
    # Esto es lo que hace el reproductor por detrás
    api_url = f"https://www.dailymotion.com/player/metadata/video/{video_id}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://www.tctelevision.com/"
    }

    try:
        print(f"📡 Pidiendo autorización a Dailymotion para {video_id}...")
        response = requests.get(api_url, headers=headers, timeout=15)
        data = response.json()
        
        # El token de seguridad 'sec' está en las cookies de la respuesta o en el JSON
        # Buscamos en las URL de las variantes de video
        qualities = data.get('qualities', {})
        # Buscamos el stream 'auto' (HLS)
        auto_stream = qualities.get('auto', [{}])[0].get('url', '')
        
        if auto_stream:
            print("✅ ¡URL de transmisión localizada!")
            return auto_stream
            
    except Exception as e:
        print(f"❌ Error en API: {e}")
    
    return None

# --- Lógica de actualización del JSON ---
archivo_json = 'canales.json'

try:
    nuevo_link = get_tc_link()
    
    if not nuevo_link:
        print("❌ No se pudo generar el link. Dailymotion pide una sesión activa.")
        sys.exit(1)

    with open(archivo_json, 'r', encoding='utf-8') as f:
        canales = json.load(f)

    for c in canales:
        if "TC" in c.get('nombre', '').upper():
            c['url'] = nuevo_link
            print(f"🚀 Link actualizado: {nuevo_link[:60]}...")
            break
            
    with open(archivo_json, 'w', encoding='utf-8') as f:
        json.dump(canales, f, indent=2, ensure_ascii=False)
        
except Exception as e:
    print(f"❌ Error crítico: {e}")
    sys.exit(1)
