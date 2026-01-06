from src.main import cargar_misiones, guardar_misiones
import os
import json

def test_persistence():
    print("Iniciando prueba de persistencia...")
    
    # 1. Cargar originales
    originales = cargar_misiones()
    count_original = len(originales)
    
    # 2. Crear misión de prueba
    test_mision = {
        "id": 999,
        "nombre": "Misión de Prueba Temporal",
        "url": "http://test.com",
        "necesita_login": False,
        "config_scraping": {
            "selector_contenedor": "div",
            "campos": {"Test": "span"},
            "limite": 1
        }
    }
    
    originales.append(test_mision)
    guardar_misiones(originales)
    
    # 3. Recargar y verificar
    nuevas = cargar_misiones()
    assert len(nuevas) == count_original + 1
    assert nuevas[-1]["nombre"] == "Misión de Prueba Temporal"
    print("✅ Inserción verificada.")
    
    # 4. Limpiar (dejar como estaba)
    originales.pop()
    guardar_misiones(originales)
    nuevas_final = cargar_misiones()
    assert len(nuevas_final) == count_original
    print("✅ Limpieza verificada.")
    print("\n--- PRUEBA DE PERSISTENCIA EXITOSA ---")

if __name__ == "__main__":
    if not os.path.exists("config/tareas.json"):
        print("Error: No se encuentra config/tareas.json")
    else:
        test_persistence()
