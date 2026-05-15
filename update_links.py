import requests
import re
import json

def get_tc_link():
    url = "https://www.tctelevision.com/en-vivo"
    # Engañamos al servidor haciéndonos pasar por un iPhone
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        # Buscamos el link que termina en .m3u8 dentro del código de la página
        match = re.search(r'https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*', response.text)
        
        if match:
            link = match.group(0).replace('\\/', '/')
            return link
    except Exception as e:
        print(f"Error: {e}")
    return None

def update_json():
    nuevo_link = get_tc_link()
    if nuevo_link:
        try:
            with open('canales.json', 'r', encoding='utf-8') as f:
                canales = json.load(f)
            
            for canal in canales:
                if canal['id'] == "10":
                    canal['url'] = nuevo_link
                    break
            
            with open('canales.json', 'w', encoding='utf-8') as f:
                json.dump(canales, f, indent=2, ensure_ascii=False)
            print("✅ Link actualizado con éxito.")
        except Exception as e:
            print(f"Error al escribir JSON: {e}")
    else:
        print("❌ No se encontró el link .m3u8")

if __name__ == "__main__":
    update_json()
