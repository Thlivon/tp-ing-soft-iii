# AQUÍ IRÁN LAS PRUEBAS PRUEBAS UNITARAS Y EN EL FUTURO SERÁ EL FRONTEND
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
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
    if "uploader_key" not in st.session_state:
        st.session_state.uploader_key = 0

def mostrar_pantalla_carga():
    """Muestra la interfaz inicial para cargar el archivo."""
    st.title("Analizador de chats de WhatsApp")
    st.write("Seleccioná tu archivo de chat exportado desde WhatsApp para comenzar el análisis.")

    archivo = st.file_uploader(
        label="Seleccioná tu archivo de chat en formato .txt o .zip",
        help="Exportá tu chat desde WhatsApp: Menú -> Más -> Exportar chat -> Sin archivos multimedia",
        key=str(st.session_state.uploader_key)
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

    # --- Fase 2.2: Visualización de Datos ---
    st.header("📊 Resumen del Chat")
    
    col1, col2 = st.columns(2)
    with col1:
        usuario, cantidad = usuario_mas_activo(df)
        st.metric(label="👑 Usuario más activo", value=str(usuario), delta=f"{cantidad} mensajes", delta_color="off")
        
    with col2:
        emoji_texto, cantidad_emoji = emoji_mas_utilizado(df)
        emoji_val = emoji_lib.emojize(emoji_texto) if emoji_texto else "Ninguno"
        st.metric(label="🔥 Emoji más usado", value=emoji_val, delta=f"{cantidad_emoji} veces", delta_color="off")
        
    st.divider()

    # --- Gráfico de Franja Horaria ---
    st.subheader("⏰ Actividad por Franja Horaria")
    franja, cantidad = horario_mas_activo(df)
    st.write(f"**Horario pico:** {franja} ({cantidad} mensajes)")
    
    # Preparamos los datos completando las 24 horas para que el gráfico sea continuo
    datos_horas = df["fecha"].dt.hour.value_counts().reindex(range(24), fill_value=0)
    datos_horas.index = [f"{h:02d}:00" for h in datos_horas.index]
    st.bar_chart(datos_horas)

    st.divider()

    # --- Gráfico de Actividad por Día ---
    st.subheader("📅 Actividad por Día de la Semana")
    col_grafico, col_ranking = st.columns([2, 1])
    
    with col_grafico:
        porcentajes = actividad_por_dia(df)
        # Traducimos los días al español para el gráfico
        dias_es = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        # Usamos CategoricalIndex para forzar el orden cronológico y evitar que Streamlit lo ordene alfabéticamente
        porcentajes.index = pd.CategoricalIndex(dias_es, categories=dias_es, ordered=True)
        st.bar_chart(porcentajes)

    with col_ranking:
        st.write("**🏆 Ranking de mayor actividad**")
        ranking = ranking_actividad(df)
        traduccion = {"Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles", "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"}
        for i, (dia, porcentaje) in enumerate(ranking.items(), 1):
            st.write(f"**{i}. {traduccion.get(dia, dia)}**: {porcentaje}%")

    st.divider()

    # --- Nube de Palabras ---
    st.subheader("☁️ Nube de Palabras")
    palabras_frecuentes = frecuencia_palabras(df)
    if palabras_frecuentes:
        wordcloud = WordCloud(width=800, height=400, background_color="white", colormap="viridis").generate_from_frequencies(palabras_frecuentes)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.info("No hay suficientes palabras para generar la nube.")

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
            if st.button("Restaurar", help="Elimina el chat actual y reinicia la aplicación"):
                st.session_state.archivo_cargado = None
                st.session_state.chat_procesado = False
                st.session_state.df_chat = None
                st.session_state.uploader_key += 1
                st.rerun()
                
            mostrar_resultados_temporales(st.session_state.df_chat)

if __name__ == "__main__":
    main()
