import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_tc_link():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Esto permite que Selenium "escuche" las peticiones de red
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        print("🌍 Entrando a TC Televisión (Interceptando red)...")
        driver.get("https://www.tctelevision.com/envivo")
        
        # Esperamos 25 segundos para que el reproductor cargue el m3u8 que viste en la extensión
        time.sleep(25)
        
        logs = driver.get_log('performance')
        
        for entry in logs:
            log = json.loads(entry['message'])['message']
            if log['method'] == 'Network.requestWillBeSent':
                url = log['params']['request']['url']
                # Buscamos el nombre de archivo exacto que te sale en The Stream Doctor
                if "x7wijay.m3u8" in url and "sec=" in url:
                    print(f"✅ ¡URL CAPTURADA!: {url[:70]}...")
                    return url

        print("❌ La red terminó de cargar pero no se detectó el link de Dailymotion.")
            
    except Exception as e:
        print(f"❌ Error en el interceptor: {e}")
    finally:
        driver.quit()
    return None

# --- Lógica de actualización de archivos ---
archivo_json = 'canales.json' # Asegúrate de que se llame así en tu repo
nuevo_link = get_tc_link()

if nuevo_link:
    with open(archivo_json, 'r', encoding='utf-8') as f:
        canales = json.load(f)
    
    actualizado = False
    for c in canales:
        if "TC" in c.get('nombre', '').upper():
            if c['url'] != nuevo_link:
                c['url'] = nuevo_link
                actualizado = True
            break
            
    if actualizado:
        with open(archivo_json, 'w', encoding='utf-8') as f:
            json.dump(canales, f, indent=2, ensure_ascii=False)
        print("🚀 ¡canales.json actualizado con éxito!")
    else:
        print("ℹ️ El link capturado es el mismo que ya estaba en el JSON.")
