import requests
import json
import re
import sys

def get_tc_link():
    video_id = "x7wijay"
    # Usamos un proxy de respaldo diferente (shrtlst)
    proxy_url = "https://api.allorigins.win/get?url="
    target_url = f"https://www.dailymotion.com/player/metadata/video/{video_id}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
        "Referer": "https://www.tctelevision.com/"
    }

    try:
        print(f"🕵️ Intentando bypass para TC (ID: {video_id})...")
        # Intentamos primero directo por si la IP de GitHub se "enfrió"
        try:
            res = requests.get(target_url, headers=headers, timeout=10)
            if res.status_code == 200:
                data = res.json()
                url = data.get('qualities', {}).get('auto', [{}])[0].get('url')
                if url:
                    print("✅ ¡Link obtenido directamente!")
                    return url
        except:
            pass

        # Si falla, vamos por el puente
        print("🌉 El directo falló, usando puente de emergencia...")
        full_url = f"{proxy_url}{requests.utils.quote(target_url)}"
        response = requests.get(full_url, timeout=15)
        
        # Limpiamos la respuesta del proxy
        content = response.json().get('contents')
        if content:
            data = json.loads(content)
            url = data.get('qualities', {}).get('auto', [{}])[0].get('url')
            if url:
                print("✅ ¡Link obtenido por el puente!")
                return url

    except Exception as e:
        print(f"❌ Error en la infiltración: {e}")
    
    return None

# --- Lógica de actualización ---
archivo_json = 'canales.json'

try:
    nuevo_link = get_tc_link()
    if not nuevo_link:
        print("💀 No hubo forma. TC bloqueó todas las rutas.")
        sys.exit(1)

    with open(archivo_json, 'r', encoding='utf-8') as f:
        canales = json.load(f)

    for c in canales:
        if "TC" in c.get('nombre', '').upper():
            c['url'] = nuevo_link
            print("🚀 canales.json actualizado.")
            break
            
    with open(archivo_json, 'w', encoding='utf-8') as f:
        json.dump(canales, f, indent=2, ensure_ascii=False)
        
except Exception as e:
    print(f"❌ Error de escritura: {e}")
    sys.exit(1)
