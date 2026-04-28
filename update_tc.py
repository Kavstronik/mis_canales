import requests
import json
import os
import sys

def get_tc_link():
    video_id = "x7wijay"
    api_url = f"https://www.dailymotion.com/player/metadata/video/{video_id}"
    
    # Extraemos la identidad real desde los Secrets de GitHub
    cookie_master = os.getenv('TC_COOKIE')
    user_agent_master = os.getenv('TC_USER_AGENT')

    if not cookie_master or not user_agent_master:
        print("❌ Error: No se configuraron los Secrets TC_COOKIE o TC_USER_AGENT en GitHub.")
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
        print("📡 Iniciando túnel de sesión con identidad clonada...")
        response = requests.get(api_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            # Capturamos el manifiesto maestro (HLS)
            stream_url = data.get('qualities', {}).get('auto', [{}])[0].get('url')
            
            if stream_url:
                print("✅ ¡LOGRADO! El link firmado ha sido generado.")
                return stream_url
        
        print(f"⚠️ Dailymotion respondió con status {response.status_code}, pero sin link. Revisa si la cookie expiró.")
    except Exception as e:
        print(f"❌ Fallo en la conexión: {e}")
    
    return None

# --- Lógica de actualización del archivo canales.json ---
archivo_json = 'canales.json'
nuevo_link = get_tc_link()

if nuevo_link:
    try:
        if os.path.exists(archivo_json):
            with open(archivo_json, 'r', encoding='utf-8') as f:
                canales = json.load(f)
        else:
            canales = []

        actualizado = False
        for c in canales:
            if "TC" in c.get('nombre', '').upper():
                c['url'] = nuevo_link
                actualizado = True
                break
        
        if not actualizado:
            canales.append({"nombre": "TC Television", "url": nuevo_link})

        with open(archivo_json, 'w', encoding='utf-8') as f:
            json.dump(canales, f, indent=2, ensure_ascii=False)
        print("🚀 canales.json actualizado exitosamente.")
    except Exception as e:
        print(f"❌ Error al procesar el archivo JSON: {e}")
else:
    sys.exit(1)
