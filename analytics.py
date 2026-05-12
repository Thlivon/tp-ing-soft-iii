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