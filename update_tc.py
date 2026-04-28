import requests
import json
import sys

def get_tc_link():
    video_id = "x7wijay"
    # Usamos un proxy para ocultar que la petición viene de GitHub
    proxy_url = "https://api.allorigins.win/get?url="
    target_url = f"https://www.dailymotion.com/player/metadata/video/{video_id}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://www.tctelevision.com/"
    }

    try:
        print(f"🌉 Usando puente para saltar el bloqueo de Dailymotion...")
        # La URL se codifica para pasar por el proxy
        full_url = f"{proxy_url}{requests.utils.quote(target_url)}"
        
        response = requests.get(full_url, headers=headers, timeout=15)
        # AllOrigins devuelve el contenido dentro de una clave llamada 'contents'
        data_raw = response.json().get('contents', '{}')
        data = json.loads(data_raw)
        
        stream_url = data.get('qualities', {}).get('auto', [{}])[0].get('url')
        
        if stream_url:
            print("✅ ¡LOGRADO! Link capturado a través del puente.")
            return stream_url
            
    except Exception as e:
        print(f"❌ El puente falló: {e}")
    
    return None

# --- Lógica de guardado ---
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
            print("🚀 JSON actualizado.")
            break
            
    with open(archivo_json, 'w', encoding='utf-8') as f:
        json.dump(canales, f, indent=2, ensure_ascii=False)
        
except Exception as e:
    print(f"❌ Error final: {e}")
    sys.exit(1)
