import requests
import json
import os
import sys

def get_tc_link():
    video_id = "x7wijay"
    # API de metadatos de Dailymotion para obtener el link firmado
    api_url = f"https://www.dailymotion.com/player/metadata/video/{video_id}"
    
    # Extraemos la identidad real desde los Secrets de GitHub
    cookie_master = os.getenv('TC_COOKIE')
    user_agent_master = os.getenv('TC_USER_AGENT')

    if not cookie_master or not user_agent_master:
        print("❌ Error: Faltan los Secrets TC_COOKIE o TC_USER_AGENT en GitHub.")
        return None

    headers = {
        "User-Agent": user_agent_master,
        "Referer": "https://geo.dailymotion.com/",
        "Origin": "https://geo.dailymotion.com",
        "Cookie": cookie_master,
        "Accept": "*/*",
        "Accept-Language": "es-EC,es;q=0.9"
    }

    try:
        print("📡 Solicitando link firmado con sesión clonada de Guayaquil...")
        response = requests.get(api_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            # El link 'auto' contiene el token sec= actualizado
            stream_url = data.get('qualities', {}).get('auto', [{}])[0].get('url')
            
            if stream_url:
                print("✅ ¡LOGRADO! Link generado correctamente.")
                return stream_url
        
        print(f"⚠️ El servidor respondió con status {response.status_code}. Es posible que la cookie haya expirado.")
    except Exception as e:
        print(f"❌ Fallo técnico en la conexión: {e}")
    
    return None

# --- Lógica para actualizar el archivo canales.json ---
archivo_json = 'canales.json'
nuevo_link = get_tc_link()

if nuevo_link:
    try:
        if os.path.exists(archivo_json):
            with open(archivo_json, 'r', encoding='utf-8') as f:
                canales = json.load(f)
        else:
            canales = []

        # Buscamos TC para actualizarlo, si no existe lo creamos
        encontrado = False
        for c in canales:
            if "TC" in c.get('nombre', '').upper():
                c['url'] = nuevo_link
                encontrado = True
                break
        
        if not encontrado:
            canales.append({"nombre": "TC Television", "url": nuevo_link})

        with open(archivo_json, 'w', encoding='utf-8') as f:
            json.dump(canales, f, indent=2, ensure_ascii=False)
        print("🚀 canales.json actualizado con éxito.")
    except Exception as e:
        print(f"❌ Error al escribir en el JSON: {e}")
else:
    # Salimos con error para que el Action se ponga rojo si falla
    sys.exit(1)
