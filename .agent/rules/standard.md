---
trigger: always_on
---

# Estándares del Proyecto Micro-SaaS

1. **Aislamiento (Entorno):** Todo el desarrollo, ejecución e instalación de librerías debe realizarse estrictamente dentro del entorno virtual activo (`.venv`).

2. **Seguridad (Zero Leak Policy):** Queda terminantemente prohibido subir archivos `.env` o hardcodear credenciales, tokens o rutas locales absolutas en el código.

3. **La Barrera de Git:** Antes de cada *commit*, se debe verificar que el archivo `.gitignore` incluya `.env`, carpetas de logs y archivos temporales (`__pycache__`).

4. **Documentación Viva:**
   - **Estructura:** Cada carpeta compleja debe tener un `README.md` breve explicando su propósito.
   - **Bitácora (MANDATORIO):** Se debe mantener actualizada la `GUIA_TECNICA_MAESTRA.md` con cada nuevo aprendizaje.

5. **Trazabilidad (Logs):** Usar `Loguru` para todo registro. Los logs deben ser sanitizados: nunca registrar contraseñas ni datos personales del cliente en caso de error.

6. **Escalabilidad de Datos:** Los datos de salida (datasets) deben procesarse preferiblemente con `Polars`. Formato estándar: CSV.

7. **Código Moderno (Type Hints):** Las funciones deben incluir "Type Hints" (ej: `def obtener_precio() -> float:`) para validar tipos de datos.

8. **Claridad Inmediata (Docstrings):** 
   Toda función o clase debe iniciar con un Docstring (`""" Texto """`) que explique en una frase **QUÉ** hace la función, y si es compleja, qué parámetros recibe (Args) y qué devuelve (Returns).

9. **Orden estructural:**
   Todos los documentos deben de colocarse en una carpeta "docs", si esta no existe, entonces se creará. Dentro de esta carpeta, siempre debe de haber una **Guía técnica** y una **Bienvenida y Mapa de Proyecto**; Siempre crear un archivo **requirements.txt** actualizable con el tiempo.