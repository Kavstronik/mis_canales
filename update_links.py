import requests
import re
import json

def get_tc_link():
    url_web = "https://www.tctelevision.com/en-vivo"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        response = requests.get(url_web, headers=headers, timeout=10)
        # Buscamos el link m3u8 que tenga el token ?sec=
        match = re.search(r'https://[\w\.-]+\.dailymotion\.com/[\w\./\?=-]+\.m3u8[\w\?=&-]+', response.text)
        return match.group(0) if match else None
    except:
        return None

def update_json():
    # 1. Leer tu archivo local
    with open('canales.json', 'r', encoding='utf-8') as f:
        canales = json.load(f)

    # 2. Obtener el link fresco
    nuevo_link = get_tc_link()
    
    if nuevo_link:
        # 3. Buscar el ID 10 (TC) y actualizarlo
        for canal in canales:
            if canal['id'] == "10":
                canal['url'] = nuevo_link
                print(f"✅ Link de TC actualizado: {nuevo_link[:50]}...")
                break
        
        # 4. Guardar los cambios
        with open('canales.json', 'w', encoding='utf-8') as f:
            json.dump(canales, f, indent=2, ensure_ascii=False)
    else:
        print("❌ No se pudo encontrar el link de TC")

if __name__ == "__main__":
    update_json()
