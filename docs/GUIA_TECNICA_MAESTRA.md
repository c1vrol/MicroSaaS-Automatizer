# Documentación Maestra: Micro-SaaS Scraper Seguro

Este documento detalla la arquitectura, decisiones de ingeniería y procedimientos operativos del proyecto.

## 1. Génesis y Comandos (El "Cómo")

La construcción se realizó siguiendo un flujo de aislamiento total:

1. **Entorno Virtual (`.venv`):** 
   - Comando: `python -m venv .venv`
   - *Razón:* Evita contaminar el Python global del sistema y asegura que las versiones de las librerías sean fijas.
2. **Instalación de STACK (PowerShell):**
   - `.\.venv\Scripts\python.exe -m pip install playwright polars python-dotenv loguru`
   - `.\.venv\Scripts\playwright install chromium` (Instala el motor de navegación específico).

## 2. Lógica del Sistema (El "Cerebro")

El script `src/main.py` funciona como una orquesta:
- **`python-dotenv`**: Actúa como el portero, leyendo secretos sin que nadie los vea.
- **`Playwright`**: Simula a un humano real navegando. Usamos selectores CSS (`.quote`, `.text`, `.author`) para "apuntar" a los datos.
- **`Polars`**: Recibe los datos en memoria y los transforma en una tabla (DataFrame), optimizando el guardado en CSV.

## 4. Gestión de Logs Persistentes (`Loguru`)

Para que un Micro-SaaS sea profesional, no basta con ver mensajes en la consola; necesitamos un historial de qué sucedió si el bot falla a las 3 AM.

### Configuración de Archivo (`logger.add`)
En `src/main.py` usamos el siguiente comando:
```python
logger.add("logs/bot_history.log", format="{time} | {level} | {message}", level="DEBUG", rotation="1 MB")
```

**Parámetros clave:**
- **`sink` ("logs/bot_history.log"):** La ruta donde se guarda el archivo.
- **`rotation="1 MB"`:** Regla de oro de Micro-SaaS. Cuando el log pesa 1MB, Loguru crea uno nuevo automáticamente. Esto evita que el disco duro se llene y que el servidor colapse.
- **`level="DEBUG"`:** En el archivo guardamos *todo* (incluso detalles técnicos), mientras que en la consola solo mostramos lo importante (`INFO`).

### ¿Por qué no usar `logging` tradicional?
- **Sintaxis:** El módulo nativo de Python es verboso y complejo de configurar. Loguru es "Ready to use".
- **Higiene:** Loguru facilita la creación de filtros para asegurar que nunca se escriban secretos del `.env` por accidente.

## 5. El Salto al 80/20 (Motor Interactivo)

Hemos evolucionado de un script rígido a un **Motor de Acciones Genérico**. Esta decisión técnica se basa en el Principio de Pareto:

- **20% de Esfuerzo:** El usuario solo modifica un archivo `JSON` (`config/tareas.json`).
- **80% de Resultados:** El bot puede adaptarse a diferentes webs sin tocar el código fuente.

### ¿Cómo funciona la Inyección Dinámica?
El nuevo `main.py` utiliza un patrón de diseño donde la lógica de navegación es independiente de los datos. 
1. **Mapeo de Campos:** Recorre el diccionario de "campos" definido en el JSON.
2. **Selectores Flexibles:** Usa `query_selector` de forma dinámica para encontrar cualquier elemento que el usuario defina.

### Ventajas de este Enfoque
- **Mantenibilidad:** Si cambias de objetivo (por ejemplo, ahora quieres extraer libros en lugar de citas), no arriesgas romper la lógica de login o de logs.
- **Escalabilidad Micro-SaaS:** Este motor permite vender "misiones" como productos independientes simplemente entregando archivos de configuración diferentes.

---
**Actualización 10:30 AM:** Implementación del menú interactivo completada. El sistema ahora soporta múltiples misiones concurrentes en el mismo entorno.

---
**Actualización 10:45 AM: Interfaz Visual (Streamlit)**
Hemos añadido una capa visual para mejorar la experiencia del usuario y evitar el uso de la terminal.

### Arquitectura de la GUI (`src/main_gui.py`)
- **DRY (Don't Repeat Yourself):** La GUI importa las funciones `ejecutar_mision` y `cargar_misiones` directamente desde `main.py`. Si la lógica de scraping cambia, la GUI se actualiza automáticamente.
- **Feedback Visual:** Implementación de `st.spinner` y `st.success` para indicar el estado de la tarea.
- **Gestión de Datos:** Integración con `Polars` para mostrar previsualizaciones de los archivos CSV generados y permitir su descarga directa.

### Cómo ejecutar
1. Asegúrate de tener instalado streamlit (`pip install streamlit`).
2. Ejecuta: `streamlit run src/main_gui.py`.
