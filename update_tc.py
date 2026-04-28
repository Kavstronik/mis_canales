import requests
import re
import json
import sys

def get_tc_link():
    url_web = "https://www.tctelevision.com/envivo"
    # User-Agent más real para evitar bloqueos
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
    }
    
    try:
        # Usamos una sesión para manejar cookies (ayuda a pasar por humano)
        session = requests.Session()
        response = session.get(url_web, headers=headers, timeout=20)
        
        # BUSQUEDA ULTRA-AGRESIVA: 
        # Buscamos cualquier cadena de texto que tenga 'sec=' seguida de 30 o más letras/números
        tokens = re.findall(r'sec=([a-zA-Z0-9_-]{30,})', response.text)
        
        if tokens:
            # Si hay varios, el último suele ser el más fresco
            token = tokens[-1]
            print(f"✅ Token detectado: {token[:15]}...")
            return f"https://cdndirector.dailymotion.com/cdn/live/video/x7wijay.m3u8?sec={token}"
        
        # Si falla, buscamos el ID de Dailymotion x7wijay y lo que venga después
        match_alt = re.search(r'x7wijay[^\s"\'\\?]+[?&]sec=([a-zA-Z0-9_-]+)', response.text)
        if match_alt:
            token = match_alt.group(1)
            return f"https://cdndirector.dailymotion.com/cdn/live/video/x7wijay.m3u8?sec={token}"

    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    return None

archivo_json = 'canales.json'

try:
    with open(archivo_json, 'r', encoding='utf-8') as f:
        lista_canales = json.load(f)

    nuevo_link = get_tc_link()
    
    if not nuevo_link:
        print("❌ ERROR: TC bloqueó la petición o cambió el código. No hay token.")
        # No salimos con error para que el Action no se vea rojo si solo es un bloqueo temporal
        sys.exit(1)

    actualizado = False
    for canal in lista_canales:
        if "TC" in canal.get('nombre', '').upper():
            if canal['url'] != nuevo_link:
                print(f"🔄 Link viejo: {canal['url'][:40]}...")
                print(f"✨ Link nuevo: {nuevo_link[:40]}...")
                canal['url'] = nuevo_link
                actualizado = True
            break
    
    if actualizado:
        with open(archivo_json, 'w', encoding='utf-8') as f:
            json.dump(lista_canales, f, indent=2, ensure_ascii=False)
        print("🚀 ¡ARCHIVO ACTUALIZADO CON ÉXITO EN EL REPOSITORIO!")
    else:
        print("ℹ️ El link ya era el mismo, no hizo falta escribir nada.")

except Exception as e:
    print(f"❌ Fallo crítico: {e}")
    sys.exit(1)
