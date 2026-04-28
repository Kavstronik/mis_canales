import requests
import json
import sys

def get_tc_link():
    video_id = "x7wijay"
    # URL de metadatos que genera los links firmados (sec=...)
    api_url = f"https://www.dailymotion.com/player/metadata/video/{video_id}"
    
    # Headers extraídos de tu cURL para engañar al firewall
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
        "Referer": "https://geo.dailymotion.com/",
        "Origin": "https://geo.dailymotion.com",
        "Accept": "*/*",
        "Accept-Language": "es-US,es-419;q=0.9,es;q=0.8,en;q=0.7",
        "Priority": "u=1, i"
    }
    
    # Estos son los tokens de acceso que copiaste de tu navegador
    cookies = {
        "v1st": "bba544ea-bf30-0dc1-67fb-78b8069e0d07",
        "ts": "257516",
        "damd": "AS3PVFLBN3umlapml9BaSlYJlnBVPh5GUhw-vT6H45H5BdOdlDMR_m5bcJOB12uep2OLb210q8VJhgSdWdw8WqfsSH5QVDPw5OX9aje_0kvT1j3omRh3Lymbqbnb8u4oBKHUQWTQbh5ReMFJrdKzWGfcmZZuai1w7ZpIb5cvP1wIYwXUSUwKV0PYPQ7pNFi3BULMBRPvGe9nutNDIUlD2GAE_XoDDEVdNYbHAOovrimkUE73VXPGyVnd6i_4GFdC5zovF0JGvM2Czf9mAPXaIUnjW7Zkw3c3TFTZjnbGhCsoeX6iV43UHB3nFi6xJrfyJzQpnVBiM9RhWJvVBnRVQOFVAqh_s2DCqpkGFJ2HSLtWKJPpJRvGT05tfJ02JFlo-gzCAyeDGlv1ET5rm44UDg"
    }

    try:
        print("🕵️ Iniciando bypass con tokens de Guayaquil...")
        session = requests.Session()
        
        # Hacemos la petición a la API con tu identidad clonada
        response = session.get(api_url, headers=headers, cookies=cookies, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            # Buscamos el stream 'auto' que es el que vimos en tu captura (live-720/480)
            stream_url = data.get('qualities', {}).get('auto', [{}])[0].get('url')
            
            if stream_url:
                print("✅ ¡SESIÓN CLONADA CON ÉXITO! Link generado.")
                # El link vendrá con el 'sec=' nuevo generado por Dailymotion
                return stream_url
        
        print(f"❌ La sesión clonada falló. Status: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Error en la conexión: {e}")
    
    return None

# --- Lógica de actualización del archivo canales.json ---
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
        print("🚀 canales.json actualizado con el nuevo token de TC.")
    except Exception as e:
        print(f"❌ Error al guardar: {e}")
else:
    sys.exit(1)
