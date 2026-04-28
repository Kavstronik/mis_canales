import json
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_tc_link():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # No abre ventana
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        print("🌍 Abriendo TC Televisión...")
        driver.get("https://www.tctelevision.com/envivo")
        
        # Esperamos 15 segundos a que el JavaScript cargue el reproductor
        time.sleep(15)
        
        # Obtenemos el código fuente YA PROCESADO por el navegador
        html = driver.page_source
        
        # Buscamos el token sec=
        match = re.search(r'sec=([a-zA-Z0-9_-]{30,})', html)
        if match:
            token = match.group(1)
            print(f"✅ Token encontrado: {token[:15]}...")
            return f"https://cdndirector.dailymotion.com/cdn/live/video/x7wijay.m3u8?sec={token}"
        else:
            print("❌ No se encontró el token en el HTML renderizado.")
            
    except Exception as e:
        print(f"❌ Error en Selenium: {e}")
    finally:
        driver.quit()
    return None

# --- Lógica de actualización del JSON ---
archivo_json = 'canales.json'
nuevo_link = get_tc_link()

if nuevo_link:
    with open(archivo_json, 'r', encoding='utf-8') as f:
        canales = json.load(f)
    
    for c in canales:
        if "TC" in c['nombre'].upper():
            c['url'] = nuevo_link
            print("🚀 Link actualizado en canales.json")
            break
            
    with open(archivo_json, 'w', encoding='utf-8') as f:
        json.dump(canales, f, indent=2, ensure_ascii=False)
