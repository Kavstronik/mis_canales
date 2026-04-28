import requests
import re
import json
import sys

def get_tc_link():
    url_web = "https://www.tctelevision.com/envivo"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url_web, headers=headers, timeout=15)
        # Buscamos cualquier cosa que se parezca al token sec= despues del ID de TC
        # Esta es la forma más agresiva de buscarlo
        match = re.search(r'x7wijay.*?sec=([a-zA-Z0-9_-]+)', response.text)
        
        if match:
            token = match.group(1)
            print(f"✅ Token encontrado: {token[:10]}...")
            return f"https://cdndirector.dailymotion.com/cdn/live/video/x7wijay.m3u8?sec={token}"
        else:
            # Plan B: Si Dailymotion cambió el formato, buscamos el link completo
            match_alt = re.search(r'https://[^\s"]+x7wijay[^\s"]+sec=[a-zA-Z0-9_-]+', response.text)
            if match_alt:
                return match_alt.group(0).replace('\\', '')
                
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    return None

archivo_json = 'canales.json'

try:
    with open(archivo_json, 'r', encoding='utf-8') as f:
        lista_canales = json.load(f)

    nuevo_link = get_tc_link()
    
    if not nuevo_link:
        print("❌ ERROR: TC volvió a cambiar el código y el script no lo detectó.")
        sys.exit(1)

    encontrado = False
    for canal in lista_canales:
        # Buscamos "TC" sin importar mayúsculas/minúsculas
        if "TC" in canal.get('nombre', '').upper():
            print(f"✅ Canal '{canal['nombre']}' localizado.")
            if canal['url'] == nuevo_link:
                print("ℹ️ El link ya está actualizado, no hace falta cambiar nada.")
            else:
                canal['url'] = nuevo_link
                encontrado = True
            break
    
    if encontrado:
        with open(archivo_json, 'w', encoding='utf-8') as f:
            json.dump(lista_canales, f, indent=2, ensure_ascii=False)
        print("🚀 ¡JSON ACTUALIZADO EXITOSAMENTE!")
    else:
        print("ℹ️ No hubo cambios necesarios en el JSON.")

except Exception as e:
    print(f"❌ Fallo crítico: {e}")
    sys.exit(1)
