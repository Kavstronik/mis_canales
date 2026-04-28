import requests
import json
import sys

def get_tc_link():
    # El ID del video de TC
    video_id = "x7wijay"
    
    # URL base de la API de metadatos (donde se genera el link real)
    api_url = f"https://www.dailymotion.com/player/metadata/video/{video_id}"
    
    # Valores extraídos de tu cURL (La "Llave Maestra")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://www.tctelevision.com/",
        "Origin": "https://www.tctelevision.com",
        "Accept": "*/*"
    }
    
    # Estas son las cookies que Dailymotion validó en tu captura
    cookies = {
        "v1st": "bba544ea-bf30-0dc1-67fb-78b8069e0d07",
        "ts": "257516",
        "damd": "AS3PVFLBN3umlapml9BaSlYJlnBVPh5GUhw-vT6H45H5BdOdlDMR_m5bcJOB12uep2OLb210q8VJhgSdWdw8WqfsSH5QVDPw5OX9aje_0kvT1j3omRh3Lymbqbnb8u4oBKHUQWTQbh5ReMFJrdKzWGfcmZZuai1w7ZpIb5cvP1wIYwXUSUwKV0PYPQ7pNFi3BULMBRPvGe9nutNDIUlD2GAE_XoDDEVdNYbHAOovrimkUE73VXPGyVnd6i_4GFdC5zovF0JGvM2Czf9mAPXaIUnjW7Zkw3c3TFTZjnbGhCsoeX6iV43UHB3nFi6xJrfyJzQpnVBiM9RhWJvVBnRVQOFVAqh_s2DCqpkGFJ2HSLtWKJPpJRvGT05tfJ02JFlo-gzCAyeDGlv1ET5rm44UDg"
    }

    try:
        print("🕵️ Clonando sesión de Guayaquil para burlar el firewall...")
        session = requests.Session()
        
        # Realizamos la petición con tu identidad clonada
        response = session.get(api_url, headers=headers, cookies=cookies, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            # Buscamos el stream 'auto' que es el manifiesto maestro
            stream_url = data.get('qualities', {}).get('auto', [{}])[0].get('url')
            
            if stream_url:
                print("✅ ¡SESIÓN ACEPTADA! Link generado correctamente.")
                # Limpiamos escapes de barras si existen
                return stream_url.replace("\\/", "/")
        
        print(f"❌ Dailymotion rechazó la sesión (Status: {response.status_code})")
        
    except Exception as e:
        print(f"❌ Error técnico: {e}")
    
    return None

# --- Lógica de guardado en el archivo JSON ---
archivo_json = 'canales.json'
nuevo_link = get_tc_link()

if nuevo_link:
    try:
        with open(archivo_json, 'r', encoding='utf-8') as f:
            canales = json.load(f)
        
        for c in canales:
            if "TC" in c.get('nombre', '').upper():
                c['url'] = nuevo_link
                print(f"🚀 Nuevo link guardado: {nuevo_link[:60]}...")
                break
                
        with open(archivo_json, 'w', encoding='utf-8') as f:
            json.dump(canales, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        print(f"❌ Error al escribir el archivo: {e}")
else:
    sys.exit(1)
