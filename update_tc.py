import requests
import json
import os
import sys

def get_tc_link():
    video_id = "x7wijay"
    api_url = f"https://www.dailymotion.com/player/metadata/video/{video_id}"
    
    # Extraemos los datos sensibles de los Secrets de GitHub para evitar bloqueos
    cookie_master = os.getenv('TC_COOKIE')
    user_agent_master = os.getenv('TC_USER_AGENT')

    if not cookie_master or not user_agent_master:
        print("❌ Error: No se encontraron los Secrets (TC_COOKIE o TC_USER_AGENT).")
        return None

    headers = {
        "User-Agent": user_agent_master,
        "Referer": "https://geo.dailymotion.com/",
        "Origin": "https://geo.dailymotion.com",
        "Cookie": cookie_master.strip(),
        "Accept": "*/*",
        "Accept-Language": "es-EC,es;q=0.9"
    }

    try:
        print("📡 Intentando bypass con identidad clonada...")
        response = requests.get(api_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            # Capturamos la URL del manifiesto que contiene el token 'sec=' actualizado
            stream_url = data.get('qualities', {}).get('auto', [{}])[0].get('url')
            
            if stream_url:
                print("✅ ¡SESIÓN VALIDADA! Link generado con éxito.")
                return stream_url
        
        print(f"⚠️ Dailymotion respondió status {response.status_code}. Es posible que la IP de GitHub esté filtrada.")
    except Exception as e:
        print(f"❌ Error técnico en el túnel: {e}")
    
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
        print("🚀 canales.json actualizado correctamente.")
    except Exception as e:
        print(f"❌ Fallo al escribir el JSON: {e}")
else:
    sys.exit(1) # Forzamos error en el Action si no hay link
