# AQUÍ IRÁ LA LÓGICA RELACIONADA AL ANÁLISIS DE DATOS
import re

# Usuario con mayor cantidad de mensajes enviados en el chat
def usuario_mas_activo(df):

    #Si el dataframe esta vacio, devuelve None y 0.
    if df.empty:
        return None, 0

    # Cuenta las veces que aparece cada usuario en el dataframe.
    contador = df["usuario"].value_counts()

    usuario = contador.idxmax()
    cantidad = contador.max()

    return usuario, cantidad

# Devuelve el emoji mas utilizado en el chat y la cantidad de veces que se ha utilizado.
def emoji_mas_utilizado(df):
    if df.empty:
        return None, 0

    contador = {}

    for mensaje in df["mensaje"]:

        # Busca emojis en formato :nombre_emoji:
        emojis = re.findall(r":[a-zA-Z0-9_&+-]+:", mensaje)

        for e in emojis:

            if e in contador:
                contador[e] += 1
            else:
                contador[e] = 1

    if not contador:
        return None, 0

    emoji_mas_usado = max(contador, key=contador.get)

    return emoji_mas_usado, contador[emoji_mas_usado]

# Devuelve la franja horaria en la que se envían más mensajes y la cantidad de mensajes enviados en esa franja.
def horario_mas_activo(df):
    if df.empty:
        return None, 0

    horas = df["fecha"].dt.hour

    contador = horas.value_counts()

    hora_inicio = contador.idxmax()
    cantidad = contador.max()

    hora_fin = (hora_inicio + 1) % 24

    franja = f"{hora_inicio:02d}:00 - {hora_fin:02d}:00"

    return franja, cantidad

# Devuelve el porcentaje de mensajes enviados en cada dia de la semana, van ordenados de lunes a domingo.
def actividad_por_dia(df):
    if df.empty:
        return {}

    dias = df["fecha"].dt.day_name()

    contador = dias.value_counts()

    orden = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    contador = contador.reindex(orden, fill_value=0)

    porcentajes = round((contador / len(df)) * 100, 2)

    return porcentajes

# Devuelve los porcentajes de actividad ordenados de mayor a menor
def ranking_actividad(df):
    if df.empty:
        return {}

    dias = df["fecha"].dt.day_name()

    contador = dias.value_counts()

    porcentajes = round((contador / len(df)) * 100, 2)

    return porcentajes

# Devuelve una lista con las palabras mas frecuentes y la frecuencia con la que aparecen
def frecuencia_palabras(df):
    if df.empty:
        return {}

    # No cuento las palabras de la lista por ser conectores, preposiciones, artículos, etc. que no aportan al análisis
    STOPWORDS = {
        "de", "la", "que", "el", "y", "a",
        "en", "un", "una", "es", "por", ":[a-zA-Z0-9_&+-]+:"
    }

    contador = {}

    for mensaje in df["mensaje"]:
        
        # Ignoro los emojis normalizados
        mensaje = re.sub(r":[a-zA-Z0-9_&+-]+:", "", mensaje)

        palabras = mensaje.lower().split()


        for palabra in palabras:
            # Ignoro los signos de puntuacion para contar las palabras
            palabra = palabra.strip(".,!?¿¡()[]{}:;\"'")

            if palabra and palabra not in STOPWORDS:

                if palabra in contador:
                    contador[palabra] += 1
                else:
                    contador[palabra] = 1

    return contador
