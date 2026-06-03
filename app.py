# AQUÍ IRÁN LAS PRUEBAS PRUEBAS UNITARAS Y EN EL FUTURO SERÁ EL FRONTEND
import streamlit as st
from parser import parse_chat, chat_a_json
from analytics import usuario_mas_activo, emoji_mas_utilizado, horario_mas_activo, actividad_por_dia, ranking_actividad, frecuencia_palabras, ordenar_frecuencias
import emoji as emoji_lib

st.set_page_config(page_title="Analizador de chats de WhatsApp", layout="wide")

def inicializar_estado():
    """Inicializa las variables de estado de la aplicación."""
    if "archivo_cargado" not in st.session_state:
        st.session_state.archivo_cargado = None

def mostrar_pantalla_carga():
    """Muestra la interfaz inicial para cargar el archivo."""
    st.title("Analizador de chats de WhatsApp")
    st.write("Seleccioná tu archivo de chat exportado desde WhatsApp para comenzar el análisis.")

    archivo = st.file_uploader(
        label="Seleccioná tu archivo de chat en formato .txt o .zip",
        help="Exportá tu chat desde WhatsApp: Menú -> Más -> Exportar chat -> Sin archivos multimedia"
    )

    with st.container():
        st.info("También podés arrastrar tu archivo directamente sobre el área de carga.")

    # Guardamos el archivo en el estado de la sesión
    st.session_state.archivo_cargado = archivo

def validar_archivo(archivo):
    """Valida que la extensión del archivo cargado sea correcta."""
    extension = archivo.name.split(".")[-1].lower()
    if extension not in ["txt", "zip"]:
        st.error("Formato no válido. Solo se aceptan archivos .txt o .zip.")
        return False
    return True

def mostrar_resultados_temporales(df):
    """Muestra temporalmente los resultados (se refactorizará en la Fase 2.2)."""
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

def main():
    inicializar_estado()
    mostrar_pantalla_carga()
    
    # Validamos si hay un archivo cargado
    if st.session_state.archivo_cargado is not None:
        validar_archivo(st.session_state.archivo_cargado)

if __name__ == "__main__":
    main()
