# AQUÍ IRÁ LA LÓGICA RELACIONADA AL PROCESAMIENTO DEL ARCHIVO
import re
import pandas as pd

# Patrón que matchea el formato estándar de exportación de WhatsApp (Android)
# Ejemplo de línea: 12/4/25, 21:03 - Nico: hola cómo andan
PATTERN = re.compile(
    r"(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2})\s-\s([^:]+):\s(.*)"
)

def parse_chat(file):
    """Lee el archivo subido y devuelve un DataFrame con columnas: fecha, usuario, mensaje."""
    lineas = file.read().decode("utf-8").splitlines()
    registros = []
    mensaje_actual = None

    for linea in lineas:
        match = PATTERN.match(linea)
        if match:
            # Si había un mensaje acumulado, lo guardamos antes de arrancar uno nuevo
            if mensaje_actual:
                registros.append(mensaje_actual)
            fecha_str = f"{match.group(1)} {match.group(2)}"
            mensaje_actual = {
                "fecha":   pd.to_datetime(fecha_str, dayfirst=True),
                "usuario": match.group(3).strip(),
                "mensaje": limpiar_mensaje(match.group(4)),
            }
        elif mensaje_actual:
            # Línea que continúa el mensaje anterior (mensaje multilínea)
            mensaje_actual["mensaje"] += f" {limpiar_mensaje(linea.strip())}"

    # Guardamos el último mensaje que quedó pendiente
    if mensaje_actual:
        registros.append(mensaje_actual)

    return pd.DataFrame(registros)

def chat_a_json(df):
    """Convierte el DataFrame del chat a una lista de diccionarios en formato JSON."""
    return df.to_dict(orient="records")

def limpiar_mensaje(texto):
    """Elimina caracteres invisibles, de control y corruptos del texto."""
    # Elimina caracteres de control Unicode excepto saltos de línea y tabulaciones
    texto = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", texto)
    # Elimina el caracter de ancho cero típico de los exports de WhatsApp
    texto = texto.replace("\u200e", "").replace("\u200f", "")
    return texto.strip()