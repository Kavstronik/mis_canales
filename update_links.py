import requests
import json

def get_direct_link():
    # El ID que saqué de tu captura de Fiddler
    video_id = "x7wijay" 
    
    # URL de la metadata de Dailymotion (esto no lo bloquean)
    api_url = f"https://www.dailymotion.com/player/metadata/video/{video_id}"
    
    try:
        response = requests.get(api_url, timeout=15)
        data = response.json()
        
        # Extraemos el link 'auto' que es el que siempre funciona
        qualities = data.get('qualities', {})
        link = qualities.get('auto', [{}])[0].get('url')
        
        if link:
            return link
    except Exception as e:
        print(f"Error obteniendo el link de Dailymotion: {e}")
    return None

def update_json():
    nuevo_link = get_direct_link()
    
    if not nuevo_link:
        print("❌ No se pudo extraer el link de la API.")
        return

    try:
        with open('canales.json', 'r', encoding='utf-8') as f:
            canales = json.load(f)

        for canal in canales:
            if canal['id'] == "10": # ID de TC en tu JSON
                canal['url'] = nuevo_link
                print(f"✅ ¡Éxito! Link actualizado: {nuevo_link[:60]}...")
                break
        
        with open('canales.json', 'w', encoding='utf-8') as f:
            json.dump(canales, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        print(f"Error actualizando el archivo: {e}")

if __name__ == "__main__":
    update_json()
