# Estándares del Proyecto Micro-SaaS

1. **Aislamiento:** Todo el desarrollo debe realizarse dentro del entorno virtual `.venv`.
2. **Secretos:** Queda terminantemente prohibido subir archivos `.env` o hardcodear credenciales.
3. **Documentación de Estructura:** Cada nueva carpeta debe contener un archivo `.md` intuitivo explicando su propósito.
4. **Logs:** Los logs deben configurarse vía `Loguru` y nunca exponer datos sensibles de entrada.
5. **Formato:** Los datos de salida deben procesarse preferiblemente con `Polars` para asegurar escalabilidad.
6. **Documentación Evolutiva y Didáctica (MANDATORIO):** 
   - Siempre que se realicen cambios o mejoras, se debe actualizar la `GUIA_TECNICA_MAESTRA.md`.
   - Esta guía debe ser el diario de aprendizaje del proyecto: debe incluir conceptos nuevos, explicaciones de funcionamiento, razonamiento técnico de las medidas tomadas y análisis de alternativas descartadas.
