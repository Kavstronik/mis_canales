import requests
import re
import json

def get_tc_link():
    # Intentamos entrar a la página de TC
    url_web = "https://www.tctelevision.com/en-vivo"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.tctelevision.com/"
    }
    
    try:
        response = requests.get(url_web, headers=headers, timeout=15)
        html = response.text

        # MÉTODO 1: Buscar link directo m3u8
        match = re.search(r'https://[\w\.-]+\.dailymotion\.com/[\w\./\?=-]+\.m3u8[\w\?=&-]+', html)
        if match:
            return match.group(0)

        # MÉTODO 2: Si el anterior falla, buscar el ID del video y pedir el link a la API de Dailymotion
        video_id_match = re.search(r'video/(x[a-zA-Z0-9]+)', html)
        if video_id_match:
            video_id = video_id_match.group(1)
            # Consultamos la API interna de Dailymotion para ese ID
            api_url = f"https://www.dailymotion.com/player/metadata/video/{video_id}"
            api_response = requests.get(api_url, headers=headers)
            data = api_response.json()
            # Extraemos el link del manifiesto hls
            return data.get('qualities', {}).get('auto', [{}])[0].get('url')

    except Exception as e:
        print(f"Error técnico: {e}")
    
    return None

def update_json():
    try:
        with open('canales.json', 'r', encoding='utf-8') as f:
            canales = json.load(f)

        nuevo_link = get_tc_link()
        
        if nuevo_link:
            for canal in canales:
                if canal['id'] == "10":
                    canal['url'] = nuevo_link
                    print(f"✅ Éxito! Nuevo link: {nuevo_link[:60]}...")
                    break
            
            with open('canales.json', 'w', encoding='utf-8') as f:
                json.dump(canales, f, indent=2, ensure_ascii=False)
        else:
            print("❌ Sigue sin encontrarse el link. TC cambió la estructura.")
    except Exception as e:
        print(f"Error al procesar JSON: {e}")

if __name__ == "__main__":
    update_json()
