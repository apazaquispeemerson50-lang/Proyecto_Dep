
import streamlit as st

st.set_page_config(
    page_title="Proyecto_Dep",
    page_icon="⚡",
    layout="wide"
)

inicio = st.Page(
    "pages/inicio.py",
    title="Inicio",
    icon="🏠",
    default=True
)

mediciones = st.Page(
    "pages/Mediciones.py",
    title="Mediciones",
    icon="📏"
)

navegacion = st.navigation(
    [inicio, mediciones],
    position="sidebar"
)

navegacion.run()
