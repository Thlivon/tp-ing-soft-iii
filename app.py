# AQUÍ IRÁN LAS PRUEBAS PRUEBAS UNITARAS Y EN EL FUTURO SERÁ EL FRONTEND
import streamlit as st
from parser import parse_chat, chat_a_json
from analytics import usuario_mas_activo, emoji_mas_utilizado, horario_mas_activo, actividad_por_dia, ranking_actividad, frecuencia_palabras, ordenar_frecuencias
import emoji as emoji_lib

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
            # Convertimos el DataFrame a JSON para uso posterior
            mensajes_json = chat_a_json(df)
            st.success(f"Chat procesado correctamente. Se encontraron {len(mensajes_json)} mensajes.")

            usuario, cantidad = usuario_mas_activo(df)
            st.subheader("Usuario más activo")
            st.write(f"{usuario} envió {cantidad} mensajes.")

            emoji_texto, cantidad = emoji_mas_utilizado(df)
            st.subheader("Emoji más usado")
            emoji = emoji_lib.emojize(emoji_texto)
            st.write(f"{emoji} usado {cantidad} veces")

            franja, cantidad = horario_mas_activo(df)
            st.subheader("Horario más activo")
            st.write(f"Entre las {franja} se enviaron {cantidad} mensajes.")

            porcentajes = actividad_por_dia(df)
            st.subheader("Actividad por día de la semana")
            st.bar_chart(porcentajes)

            ranking = ranking_actividad(df)
            st.subheader("Ranking de actividad por día de la semana")
            for dia, porcentaje in ranking.items():
                st.write(f"{dia}: {porcentaje}%")

            palabras_frecuentes = frecuencia_palabras(df)
            st.subheader("Palabras más frecuentes")
            for palabra, frec in palabras_frecuentes.items():
                st.write(f"{palabra}: {frec} veces")

            palabras_ordenadas = ordenar_frecuencias(palabras_frecuentes)
            st.subheader("Palabras más frecuentes ordenadas")
            for palabra, frec in palabras_ordenadas:
                st.write(f"{palabra}: {frec} veces")



