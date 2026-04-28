import requests
import re
import json
import sys

def get_tc_link():
    url_web = "https://www.tctelevision.com/envivo"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        response = requests.get(url_web, headers=headers, timeout=10)
        match = re.search(r'x7wijay\?sec=([a-zA-Z0-9_-]+)', response.text)
        if match:
            token = match.group(1)
            return f"https://cdndirector.dailymotion.com/cdn/live/video/x7wijay.m3u8?sec={token}"
    except Exception as e:
        print(f"❌ Error al entrar a la web de TC: {e}")
    return None

archivo_json = 'canales.json'

try:
    with open(archivo_json, 'r', encoding='utf-8') as f:
        lista_canales = json.load(f)
    
    print(f"DEBUG: Leídos {len(lista_canales)} canales del JSON.")

    nuevo_link = get_tc_link()
    if not nuevo_link:
        print("❌ ERROR: No se pudo extraer el link de la web.")
        sys.exit(1)

    print(f"DEBUG: Link fresco obtenido: {nuevo_link[:50]}...")

    encontrado = False
    for canal in lista_canales:
        # Aquí está el truco: limpiamos espacios y comparamos
        nombre_limpio = canal.get('nombre', '').strip()
        print(f"DEBUG: Comparando '{nombre_limpio}' con 'TC Televisión'")
        
        if "TC" in nombre_limpio:
            print(f"✅ ¡COINCIDENCIA ENCONTRADA! Cambiando link viejo por el nuevo.")
            canal['url'] = nuevo_link
            encontrado = True
            break
    
    if encontrado:
        with open(archivo_json, 'w', encoding='utf-8') as f:
            json.dump(lista_canales, f, indent=2, ensure_ascii=False)
        print("🚀 JSON sobreescrito localmente con éxito.")
    else:
        print("❌ ERROR: El script no encontró ningún canal llamado 'TC Televisión' en tu lista.")
        sys.exit(1)

except Exception as e:
    print(f"❌ Fallo crítico: {e}")
    sys.exit(1)
