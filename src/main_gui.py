import streamlit as st
import polars as pl
import os
import json
from main import cargar_misiones, ejecutar_mision, setup_environment, guardar_misiones
from loguru import logger

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Moto-Bot 80/20 GUI",
    page_icon="🤖",
    layout="wide"
)

# 2. ESTILOS PERSONALIZADOS
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
    }
    .btn-exec { background-color: #28a745 !important; color: white !important; }
    .btn-save { background-color: #007bff !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# 3. LÓGICA DE LA INTERFAZ
def main():
    st.title("🤖 Motor de Automatización 80/20")
    st.markdown("---")

    # Sidebar para configuración
    st.sidebar.header("⚙️ Configuración")
    misiones = cargar_misiones()
    user, password = setup_environment()
    st.sidebar.success(f"Sesión: **{user}**")
    
    # 3.1. GESTIÓN DE MISIONES
    st.sidebar.subheader("📂 Gestión")
    modo = st.sidebar.radio("Modo:", ["Ejecutar", "Editar / Crear"])

    if modo == "Ejecutar":
        # SELECTOR DE MISIÓN
        st.subheader("📋 Misiones Disponibles")
        nombres_misiones = [m["nombre"] for m in misiones]
        seleccion = st.selectbox("Elige una misión para ejecutar:", nombres_misiones)
        mision_actual = next(m for m in misiones if m["nombre"] == seleccion)

        # Detalles
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**URL:** {mision_actual['url']}")
            st.info(f"**Login:** {'Sí' if mision_actual['necesita_login'] else 'No'}")
        
        with col2:
            st.write("**Campos:**")
            st.code(", ".join(mision_actual["config_scraping"]["campos"].keys()))

        if st.button("🚀 Iniciar Scraping", key="btn_run"):
            with st.spinner(f"Extrayendo datos de {seleccion}..."):
                ejecutar_mision(mision_actual, user, password)
                st.success(f"✅ ¡Éxito! Datos guardados.")
                
                filename = f"data/resultado_{mision_actual['id']}.csv"
                if os.path.exists(filename):
                    df = pl.read_csv(filename)
                    st.dataframe(df, use_container_width=True)
                    with open(filename, "rb") as f:
                        st.download_button("📥 Descargar CSV", f, file_name=f"resultado_{mision_actual['id']}.csv")

    else:
        # EDITOR DE MISIONES
        st.subheader("🛠️ Editor Dinámico de Misiones")
        
        nombres_misiones = ["+ NUEVA MISIÓN"] + [m["nombre"] for m in misiones]
        mision_nombre = st.selectbox("Misión a editar:", nombres_misiones)
        
        if mision_nombre == "+ NUEVA MISIÓN":
            m_id = max([m["id"] for m in misiones], default=0) + 1
            mision_base = {
                "id": m_id,
                "nombre": "Nueva Misión",
                "url": "https://example.com",
                "necesita_login": False,
                "config_scraping": {
                    "selector_contenedor": ".item",
                    "campos": {"Titulo": ".title"},
                    "limite": 10
                }
            }
        else:
            mision_base = next(m for m in misiones if m["nombre"] == mision_nombre)

        # Formulario
        with st.form("form_mision"):
            col_a, col_b = st.columns(2)
            with col_a:
                nombre = st.text_input("Nombre de la Misión", mision_base["nombre"])
                url = st.text_input("URL Objetivo", mision_base["url"])
                login = st.checkbox("¿Requiere Login?", mision_base["necesita_login"])
            
            with col_b:
                selector_cont = st.text_input("Selector del Contenedor", mision_base["config_scraping"]["selector_contenedor"])
                limite = st.number_input("Límite de ítems", 1, 100, mision_base["config_scraping"]["limite"])
            
            # Edición de campos (JSON format por simplicidad y flexibilidad)
            campos_json = st.text_area("Campos a extraer (Formato JSON)", 
                                    json.dumps(mision_base["config_scraping"]["campos"], indent=4))
            
            if st.form_submit_button("💾 Guardar Configuración"):
                try:
                    nuevos_campos = json.loads(campos_json)
                    nueva_mision = {
                        "id": mision_base["id"],
                        "nombre": nombre,
                        "url": url,
                        "necesita_login": login,
                        "config_scraping": {
                            "selector_contenedor": selector_cont,
                            "campos": nuevos_campos,
                            "limite": limite
                        }
                    }
                    
                    # Actualizar lista
                    if mision_nombre == "+ NUEVA MISIÓN":
                        misiones.append(nueva_mision)
                    else:
                        misiones = [nueva_mision if m["id"] == mision_base["id"] else m for m in misiones]
                    
                    guardar_misiones(misiones)
                    st.success("✅ Misión guardada exitosamente. Cambia al modo 'Ejecutar' para probarla.")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error en el formato de campos: {e}")

    st.markdown("---")
    st.caption("🤖 Bot Engine 80/20 • Modular & Dinámico")

if __name__ == "__main__":
    main()
