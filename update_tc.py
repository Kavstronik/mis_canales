import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def get_tc_link():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        print("🌍 Iniciando interceptor de red para TC...")
        driver.get("https://www.tctelevision.com/envivo")
        
        # Simulamos movimiento humano para despertar el reproductor
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(2)

        # Intentamos encontrar el botón de Play si existe o hacer clic en el área del video
        try:
            video_area = driver.find_element(By.TAG_NAME, "body")
            video_area.click()
            print("🖱️ Clic enviado para activar reproductor.")
        except:
            pass

        print("🔍 Monitoreando tráfico de red por 30 segundos...")
        for _ in range(15): # Revisamos cada 2 segundos
            time.sleep(2)
            logs = driver.get_log('performance')
            for entry in logs:
                log = json.loads(entry['message'])['message']
                if log['method'] == 'Network.requestWillBeSent':
                    url = log['params']['request']['url']
                    # Buscamos exactamente el patrón de tu extensión
                    if "x7wijay.m3u8" in url and "sec=" in url:
                        print(f"✅ ¡LINK CAPTURADO!: {url[:70]}...")
                        return url
    
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        driver.quit()
    return None

# --- Bloque de guardado ---
archivo_json = 'canales.json'
nuevo_link = get_tc_link()

if nuevo_link:
    with open(archivo_json, 'r', encoding='utf-8') as f:
        canales = json.load(f)
    
    for c in canales:
        if "TC" in c.get('nombre', '').upper():
            c['url'] = nuevo_link
            print("🚀 Guardado en canales.json")
            break
            
    with open(archivo_json, 'w', encoding='utf-8') as f:
        json.dump(canales, f, indent=2, ensure_ascii=False)
else:
    print("❌ No se pudo capturar el link. TC sigue bloqueando el tráfico automático.")
