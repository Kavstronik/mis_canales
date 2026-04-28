import json
import time
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_tc_link():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        print("🌍 Buscando vulnerabilidad en el Frame de TC...")
        driver.get("https://www.tctelevision.com/envivo")
        time.sleep(10)
        
        # Buscamos el link de Dailymotion escondido en los iFrames
        iframes = driver.find_elements("tag name", "iframe")
        dm_url = ""
        for iframe in iframes:
            src = iframe.get_attribute("src")
            if src and "dailymotion.com/embed/video/x7wijay" in src:
                dm_url = src
                break
        
        if dm_url:
            print(f"🔗 Frame de video localizado. Extrayendo token...")
            # Entramos directo al link del embed para que no nos bloquee la web de TC
            driver.get(dm_url)
            time.sleep(5)
            
            # El token 'sec' suele estar en una variable de JavaScript llamada 'config' o 'internalData'
            script_content = driver.page_source
            token_match = re.search(r'sec\\":\\"([a-zA-Z0-9_-]+)\\"', script_content)
            
            if token_match:
                token = token_match.group(1)
                print(f"✅ TOKEN EXTRAÍDO: {token[:15]}...")
                return f"https://cdndirector.dailymotion.com/cdn/live/video/x7wijay.m3u8?sec={token}"
        
        print("❌ El Frame no soltó el token. Intentando método de emergencia...")
        # Si todo falla, buscamos en el texto plano del embed
        res = requests.get(dm_url, headers={"User-Agent": chrome_options.arguments[-1].split('=')[1]})
        token_alt = re.search(r'"sec":"([a-zA-Z0-9_-]+)"', res.text)
        if token_alt:
            return f"https://cdndirector.dailymotion.com/cdn/live/video/x7wijay.m3u8?sec={token_alt.group(1)}"

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        driver.quit()
    return None

# --- Guardado ---
archivo_json = 'canales.json'
nuevo_link = get_tc_link()

if nuevo_link:
    with open(archivo_json, 'r', encoding='utf-8') as f:
        canales = json.load(f)
    for c in canales:
        if "TC" in c.get('nombre', '').upper():
            c['url'] = nuevo_link
            print("🚀 Actualización exitosa.")
            break
    with open(archivo_json, 'w', encoding='utf-8') as f:
        json.dump(canales, f, indent=2, ensure_ascii=False)
else:
    print("❌ TC ganó esta ronda. El token está blindado.")
