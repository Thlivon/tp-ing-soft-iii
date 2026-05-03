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

    for linea in lineas:
        match = PATTERN.match(linea)
        if match:
            fecha_str = f"{match.group(1)} {match.group(2)}"
            registros.append({
                "fecha":   pd.to_datetime(fecha_str, dayfirst=True),
                "usuario": match.group(3).strip(),
                "mensaje": match.group(4),
            })

    return pd.DataFrame(registros)