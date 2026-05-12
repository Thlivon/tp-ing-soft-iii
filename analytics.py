# AQUÍ IRÁ LA LÓGICA RELACIONADA AL ANÁLISIS DE DATOS

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