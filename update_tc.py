import requests
import json
import sys
import re

def get_tc_link():
    video_id = "x7wijay"
    # Esta es la URL base que sacamos de tu extensión
    base_url = f"https://dmxleo.dailymotion.com/cdn/manifest/video/{video_id}.m3u8"
    
    # Parámetros que vimos en tu captura para que Dailymotion nos crea
    params = {
        "bs": "1",
        "rid": "0",
        "cookie_sync_ab_gk": "1",
        "reader_gdpr_flag": "0",
        "gdpr_binary_consent": "opt-out",
        "gdpr_comes_from_infopack": "0",
        "reader_us_privacy": "1---",
        "eb": "https://tctelevision.com/" # El parámetro crucial
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://tctelevision.com/",
        "Origin": "https://tctelevision.com"
    }

    try:
        print(f"📡 Intentando validar el link de extensión para {video_id}...")
        
        # Primero hacemos un 'head' para ver si Dailymotion nos da el OK
        response = requests.head(base_url, params=params, headers=headers, timeout=10)
        
        # Si nos da un 200 o un 302, el link es válido
        if response.status_code in [200, 302]:
            # Construimos la URL final con los parámetros
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            final_url = f"{base_url}?{query_string}"
            print("✅ ¡Link validado y generado!")
            return final_url
        
        # Plan B: Si el anterior falla, intentamos pescar el 'sec' del HTML
        print("⚠️ Link directo rechazado, buscando token 'sec' alternativo...")
        res_web = requests.get("https://www.tctelevision.com/envivo", headers=headers)
        token_match = re.search(r'"sec":"([a-zA-Z0-9_-]+)"', res_web.text)
        if token_match:
            return f"https://cdndirector.dailymotion.com/cdn/live/video/{video_id}.m3u8?sec={token_match.group(1)}"

    except Exception as e:
        print(f"❌ Error: {e}")
    
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
        print("🚀 ¡canales.json actualizado con el formato de la extensión!")
    except Exception as e:
        print(f"❌ Error al guardar: {e}")
else:
    print("❌ No se pudo generar un link válido esta vez.")
    sys.exit(1)
