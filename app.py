# AQUÍ IRÁN LAS PRUEBAS PRUEBAS UNITARAS Y EN EL FUTURO SERÁ EL FRONTEND
import streamlit as st

st.set_page_config(page_title="Analizador de chats de WhatsApp", layout="wide")

st.title("Analizador de chats de WhatsApp")
st.write("Seleccioná tu archivo de chat exportado desde WhatsApp para comenzar el análisis.")

# Widget que permite al usuario seleccionar un archivo desde el explorador de archivos
archivo = st.file_uploader(
    label="Seleccioná tu archivo de chat",
    help="Exportá tu chat desde WhatsApp: Menú -> Más -> Exportar chat -> Sin archivos multimedia"
)

# Sección visual que indica al usuario que también puede arrastrar el archivo
with st.container():
    st.info("También podés arrastrar tu archivo directamente sobre el área de carga.")

# Si el usuario seleccionó un archivo, mostramos su nombre como confirmación
if archivo is not None:
    st.success(f"Archivo seleccionado: {archivo.name}")