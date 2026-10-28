
import streamlit as st

st.set_page_config(
    page_title="Proyecto_Dep",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Proyecto_Dep")
st.subheader("Sistema de registro y cálculo de mediciones")

st.write(
    """
    Bienvenido al sistema de mediciones.

    Esta plataforma permitirá al personal de campo y de oficina
    registrar datos, realizar cálculos y consultar resultados.
    """
)

st.divider()

st.markdown("### 📋 Módulos disponibles")

col1, col2 = st.columns(2)

with col1:
    st.info(
        "**📏 Control de Mediciones**\n\n"
        "Registra mediciones de campo, calcula diferencias "
        "y revisa desviaciones."
    )

with col2:
    st.info(
        "**📊 Próximos módulos**\n\n"
        "Aquí podremos agregar nuevos formularios, "
        "indicadores y reportes."
    )

st.success(
    "Aplicación operativa. Selecciona "
    "'Mediciones' en el menú lateral para comenzar."
)

st.caption("Proyecto_Dep | Prototipo inicial")
