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
    if "chat_procesado" not in st.session_state:
        st.session_state.chat_procesado = False
    if "df_chat" not in st.session_state:
        st.session_state.df_chat = None

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

    # Si el archivo cambia, actualizamos el estado y reiniciamos el procesamiento
    if st.session_state.archivo_cargado != archivo:
        st.session_state.archivo_cargado = archivo
        st.session_state.chat_procesado = False
        st.session_state.df_chat = None

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
        es_valido = validar_archivo(st.session_state.archivo_cargado)
        
        if es_valido and not st.session_state.chat_procesado:
            if st.button("Procesar archivo", type="primary"):
                with st.spinner("Procesando el chat, por favor esperá..."):
                    df = parse_chat(st.session_state.archivo_cargado)
                    if not df.empty:
                        st.session_state.df_chat = df
                        st.session_state.chat_procesado = True
                        st.rerun()
                    else:
                        st.warning("No se encontraron mensajes. Verificá que el archivo sea un chat válido.")
                    
        if st.session_state.chat_procesado:
            mostrar_resultados_temporales(st.session_state.df_chat)

if __name__ == "__main__":
    main()
