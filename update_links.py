import requests
import json

def get_tc_live_link():
    # ID del canal en vivo de TC en Dailymotion
    video_id = "x7wijay" 
    api_url = f"https://www.dailymotion.com/player/metadata/video/{video_id}"
    
    try:
        response = requests.get(api_url, timeout=15)
        data = response.json()
        
        # Dailymotion entrega el m3u8 en la sección 'qualities'
        # Buscamos la URL de 'auto' que es la que se adapta al internet
        m3u8_url = data.get('qualities', {}).get('auto', [{}])[0].get('url')
        
        return m3u8_url
    except Exception as e:
        print(f"Error técnico: {e}")
    return None

def update_json():
    nuevo_link = get_tc_live_link()
    
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
            print(f"✅ Link capturado: {nuevo_link[:50]}...")
        except Exception as e:
            print(f"Error al guardar: {e}")
    else:
        print("❌ Dailymotion bloqueó la petición.")

if __name__ == "__main__":
    update_json()
