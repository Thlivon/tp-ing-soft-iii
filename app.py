# AQUÍ IRÁN LAS PRUEBAS PRUEBAS UNITARAS Y EN EL FUTURO SERÁ EL FRONTEND
import streamlit as st
from parser import parse_chat

st.set_page_config(page_title="Analizador de chats de WhatsApp", layout="wide")

st.title("Analizador de chats de WhatsApp")
st.write("Seleccioná tu archivo de chat exportado desde WhatsApp para comenzar el análisis.")

# Widget que permite al usuario seleccionar un archivo desde el explorador de archivos
archivo = st.file_uploader(
    label="Seleccioná tu archivo de chat en formato .txt o .zip",
    type=["txt", "zip"],
    help="Exportá tu chat desde WhatsApp: Menú -> Más -> Exportar chat -> Sin archivos multimedia"
)

# Sección visual que indica al usuario que también puede arrastrar el archivo
with st.container():
    st.info("También podés arrastrar tu archivo directamente sobre el área de carga.")

# Si el usuario seleccionó un archivo, mostramos su nombre como confirmación.
# Además, si el archivo tiene un formato inválido, muestra un mensaje de error.
if archivo is not None:
    extension = archivo.name.split(".")[-1].lower()
    if extension not in ["txt", "zip"]:
        st.error("Formato no válido. Solo se aceptan archivos .txt o .zip.")
    else:
        # Procesamos el archivo y convertimos el chat en un DataFrame
        df = parse_chat(archivo)

        if df.empty:
            st.warning("No se encontraron mensajes. Verificá que el archivo sea un chat de WhatsApp válido.")
        else:
            st.success(f"Chat procesado correctamente. Se encontraron {len(df)} mensajes.")