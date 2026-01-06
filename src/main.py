import os
import json
import polars as pl
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from loguru import logger
import sys

# 1. CONFIGURACIÓN DE SEGURIDAD Y LOGS
logger.remove()
logger.add(sys.stderr, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>", level="INFO")
logger.add("logs/bot_history.log", format="{time} | {level} | {message}", level="DEBUG", rotation="1 MB")

def setup_environment():
    """Carga secretos y configuraciones"""
    load_dotenv()
    user = os.getenv("USER_LOGIN")
    password = os.getenv("USER_PASSWORD")
    
    if not user or not password:
        logger.error("CRÍTICO: Credenciales ausentes en .env")
        sys.exit(1)
    
    return user, password

def cargar_misiones():
    """Lee el archivo JSON de configuración"""
    try:
        with open("config/tareas.json", "r", encoding="utf-8") as f:
            return json.load(f)["misiones"]
    except Exception as e:
        logger.error(f"Error al leer config/tareas.json: {e}")
        sys.exit(1)

def ejecutar_mision(mision, user, password):
    """Lógica genérica de ejecución de misiones"""
    logger.info(f"--- Iniciando Misión: {mision['nombre']} ---")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # NAVEGACIÓN
            page.goto(mision["url"], timeout=30000)
            
            # LOGIN (Solo si la misión lo requiere)
            if mision.get("necesita_login"):
                logger.info("Autenticando usuario...")
                page.fill('input[name="username"]', user)
                page.fill('input[name="password"]', password)
                page.click('input[type="submit"]')
                
                if not page.query_selector('a[href="/logout"]'):
                    logger.error("Fallo de login en esta misión.")
                    return

            # EXTRACCIÓN DINÁMICA
            logger.info("Extrayendo datos según configuración...")
            config = mision["config_scraping"]
            resultados = []
            
            elementos = page.query_selector_all(config["selector_contenedor"])[:config.get("limite", 99)]
            
            for el in elementos:
                fila = {}
                for nombre_campo, selector in config["campos"].items():
                    target = el.query_selector(selector)
                    fila[nombre_campo] = target.inner_text().strip() if target else "N/A"
                resultados.append(fila)

            # GUARDADO
            if resultados:
                df = pl.DataFrame(resultados)
                filename = f"data/resultado_{mision['id']}.csv"
                df.write_csv(filename)
                logger.success(f"Misión completada. Datos en: {filename}")
            else:
                logger.warning("No se encontraron datos con los selectores proporcionados.")

        except Exception as e:
            logger.error(f"Error técnico en la misión: {mision['nombre']}")
            logger.debug(f"Detalle: {str(e)}")
        finally:
            browser.close()

def mostrar_menu():
    """Interfaz interactiva para el usuario"""
    misiones = cargar_misiones()
    user, password = setup_environment()
    
    while True:
        print("\n" + "="*40)
        print("   🤖 MOTOR DE AUTOMATIZACIÓN 80/20   ")
        print("="*40)
        for i, m in enumerate(misiones):
            print(f"{i+1}. {m['nombre']}")
        print("0. Salir")
        print("="*40)
        
        opcion = input("Elige una misión para ejecutar (0-N): ")
        
        if opcion == "0":
            print("Saliendo del sistema...")
            break
        
        try:
            idx = int(opcion) - 1
            if 0 <= idx < len(misiones):
                ejecutar_mision(misiones[idx], user, password)
            else:
                print("❌ Opción inválida.")
        except ValueError:
            print("❌ Por favor, introduce un número.")

if __name__ == "__main__":
    mostrar_menu()
