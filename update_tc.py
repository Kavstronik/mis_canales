import requests
import json
import re
import sys

def get_tc_link():
    video_id = "x7wijay"
    # URL de la página que contiene el reproductor
    url_embed = f"https://www.dailymotion.com/embed/video/{video_id}?autoplay=1"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://www.tctelevision.com/",
        "Origin": "https://www.tctelevision.com"
    }

    try:
        print("📡 Iniciando rastreo de manifiesto para TC...")
        session = requests.Session()
        # 1. Obtenemos el código fuente del embed para buscar el 'metadata'
        response = session.get(url_embed, headers=headers, timeout=15)
        
        # Buscamos la URL del manifiesto maestro en el JSON interno de Dailymotion
        # Buscamos patrones de URL que terminen en .m3u8
        m3u8_links = re.findall(r'https://[^\s"\'\\]+?\.m3u8[^\s"\'\\]*', response.text)
        
        if m3u8_links:
            # Filtramos para obtener el que parece ser el stream principal
            # Generalmente contiene '/live/' o el ID del video
            for link in m3u8_links:
                if video_id in link or "/live/" in link:
                    # Limpiamos escapes de caracteres de Python si existen
                    final_link = link.replace("\\/", "/")
                    print(f"✅ ¡Manifiesto capturado!: {final_link[:50]}...")
                    return final_link

        print("❌ El rastro del manifiesto se perdió en el HTML.")
            
    except Exception as e:
        print(f"❌ Error en la conexión de red: {e}")
    
    return None

# --- Lógica de actualización del archivo ---
archivo_json = 'canales.json'

try:
    nuevo_link = get_tc_link()
    if not nuevo_link:
        sys.exit(1)

    with open(archivo_json, 'r', encoding='utf-8') as f:
        canales = json.load(f)

    actualizado = False
    for c in canales:
        if "TC" in c.get('nombre', '').upper():
            c['url'] = nuevo_link
            actualizado = True
            break
            
    if actualizado:
        with open(archivo_json, 'w', encoding='utf-8') as f:
            json.dump(canales, f, indent=2, ensure_ascii=False)
        print("🚀 canales.json actualizado exitosamente.")
    else:
        print("⚠️ No se encontró la entrada de TC en el JSON.")

except Exception as e:
    print(f"❌ Fallo crítico al procesar: {e}")
    sys.exit(1)
