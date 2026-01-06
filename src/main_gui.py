import streamlit as st
import polars as pl
import os
from main import cargar_misiones, ejecutar_mision, setup_environment
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
        background-color: #007bff;
        color: white;
    }
    .stSuccess {
        background-color: #d4edda;
        border-color: #c3e6cb;
        color: #155724;
    }
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

    st.sidebar.success(f"Conectado como: **{user}**")
    
    # Selector de misión
    st.subheader("📋 Misiones Disponibles")
    nombres_misiones = [m["nombre"] for m in misiones]
    seleccion = st.selectbox("Elige una misión para ejecutar:", nombres_misiones)
    
    mision_actual = next(m for m in misiones if m["nombre"] == seleccion)

    # Mostrar detalles de la misión seleccionada
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**URL:** {mision_actual['url']}")
        st.info(f"**Login Requerido:** {'Sí' if mision_actual['necesita_login'] else 'No'}")
    
    with col2:
        st.write("**Campos a extraer:**")
        for campo in mision_actual["config_scraping"]["campos"].keys():
            st.code(campo)

    st.markdown("---")

    # Botón de ejecución
    if st.button("🚀 Ejecutar Misión"):
        with st.spinner(f"Ejecutando {seleccion}..."):
            try:
                ejecutar_mision(mision_actual, user, password)
                st.success(f"✅ Misión '{seleccion}' completada con éxito.")
                
                # Intentar cargar resultados
                filename = f"data/resultado_{mision_actual['id']}.csv"
                if os.path.exists(filename):
                    st.subheader("📊 Último Resultado")
                    df = pl.read_csv(filename)
                    st.dataframe(df, use_container_width=True)
                    
                    # Botón de descarga
                    with open(filename, "rb") as f:
                        st.download_button(
                            label="📥 Descargar CSV",
                            data=f,
                            file_name=os.path.basename(filename),
                            mime="text/csv"
                        )
                else:
                    st.warning("⚠️ No se generó archivo de resultados.")
                    
            except Exception as e:
                st.error(f"❌ Error durante la ejecución: {e}")
                logger.error(f"Error en GUI: {e}")

    # Pie de página
    st.markdown("---")
    st.caption("Desarrollado con Streamlit • Micro-SaaS Scraper Seguro")

if __name__ == "__main__":
    main()
