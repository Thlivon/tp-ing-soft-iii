# Analizador de Chats de WhatsApp

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red)

Aplicación web que procesa archivos de exportación de WhatsApp y genera un dashboard interactivo con estadísticas y visualizaciones sobre la actividad del chat.

> Trabajo Práctico — Ingeniería de Software III

---

## Descripción general

La aplicación permite cargar un archivo de chat exportado desde WhatsApp (`.txt` o `.zip`) y analiza automáticamente su contenido para mostrar métricas clave sobre la participación y los patrones de uso del grupo.

Está inspirada en herramientas como [whatsanalyze.com](https://whatsanalyze.com/) y fue desarrollada como proyecto académico para la materia Ingeniería de Software III.

---

## Funcionalidades

### Análisis incluidos
| # | Funcionalidad | Descripción |
|---|---------------|-------------|
| 1 | 👑 Usuario más activo | Participante con mayor cantidad de mensajes enviados |
| 2 | 🔥 Emoji más utilizado | Emoji con mayor frecuencia de aparición en el chat |
| 3 | ⏰ Franja horaria con mayor actividad | Hora del día con más mensajes, con gráfico de barras (0–23 hs) |
| 4 | 📅 Días con mayor actividad | Distribución porcentual y ranking por día de la semana |
| 5 | ☁️ Nube de palabras | Visualización de las palabras más frecuentes, con filtrado de stopwords |

### Funcionalidades adicionales
- Exportación del chat procesado a formato JSON
- Soporte para archivos comprimidos (`.zip`)
- Gestión de sesión: permite recargar o resetear el chat sin reiniciar la app
- Validación del formato del archivo antes de procesar

---

## Arquitectura y decisiones técnicas

### Módulos del proyecto

```
app.py       →  Interfaz de usuario (Streamlit)
parser.py    →  Lectura, parsing y normalización del archivo
analytics.py →  Funciones de análisis estadístico
```

**`app.py`** gestiona la carga de archivos, el estado de sesión y la presentación de resultados. Delega toda la lógica a los módulos de soporte.

**`parser.py`** se encarga de leer el archivo exportado, aplicar la expresión regular para extraer campos, y limpiar el texto de caracteres de control y marcas Unicode invisibles (zero-width spaces, etc.). Incluye un fallback de encoding UTF-8 → Latin-1 para archivos exportados en dispositivos con configuración regional distinta.

**`analytics.py`** recibe un DataFrame con el chat ya parseado y expone funciones puras para cada métrica. Este diseño facilita el testing unitario de cada análisis de forma independiente.

### Elección de tecnologías

| Decisión | Alternativas consideradas | Justificación |
|----------|--------------------------|---------------|
| **Streamlit** como framework web | Flask + Jinja, Django | No requiere separar frontend y backend; el prototipo funcional se logra con código Python puro |
| **pandas** para el procesamiento | CSV nativo, listas de dicts | Operaciones de agrupación y filtrado sobre el chat son directas con DataFrames |
| **wordcloud + matplotlib** | Plotly, Altair | Integración directa con Streamlit sin configuración adicional |
| **emoji** para normalización | regex manual | Maneja correctamente variantes y secuencias de emoji con soporte Unicode actualizado |

### Formato de chat soportado

El sistema procesa el formato estándar de exportación de WhatsApp Android:

```
DD/MM/YY, HH:MM - Usuario: Mensaje
```

Los mensajes multilinea (saltos de línea dentro de un mismo mensaje) son detectados y concatenados correctamente al mensaje anterior.

---

## Estructura del proyecto

```
tp-ing-soft-iii/
├── app.py               # Interfaz Streamlit principal
├── parser.py            # Lectura y normalización del chat
├── analytics.py         # Funciones de análisis estadístico
├── requirements.txt     # Dependencias Python
└── tests/               # Casos de prueba manuales organizados por categoría
    ├── pruebas_analiticas/   # Validación de resultados analíticos
    ├── pruebas_calidad/      # Normalización: tildes, emojis, encodings, etc.
    ├── pruebas_formato/      # Tipos de archivo válidos e inválidos
    ├── pruebas_integrales/   # Flujo completo de extremo a extremo
    ├── pruebas_interfaz/     # Comportamiento de la UI
    ├── pruebas_json/         # Exportación a JSON
    ├── pruebas_rendimiento/  # Tiempos de respuesta con archivos grandes
    ├── pruebas_resultados/   # Coherencia de los resultados mostrados
    ├── pruebas_seguridad/    # Archivos malformados, contenido inesperado
    └── pruebas_subida/       # Carga de archivos desde la interfaz
```

Cada categoría contiene una carpeta `archivos_prueba/` con los archivos de entrada y un archivo `.xlsx` con los casos de prueba documentados (ID, descripción, pasos, resultado esperado, resultado obtenido, estado).

---

## Requisitos e instalación

**Requisito previo:** Python 3.8 o superior instalado en el sistema.

### 1. Clonar el repositorio

```bash
git clone https://github.com/Thlivon/tp-ing-soft-iii.git
cd tp-ing-soft-iii
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv venv
```

En Windows:
```bash
venv\Scripts\activate
```

En macOS / Linux:
```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación se abre automáticamente en el navegador en `http://localhost:8501`.

---

## Uso de la aplicación

1. **Obtener el archivo de exportación:** En WhatsApp, abrí el grupo → Menú (⋮) → Más → Exportar chat → Sin archivos multimedia. Esto genera un archivo `.txt` (o `.zip` según el dispositivo).
2. **Cargar el archivo:** En la barra lateral de la app, hacé clic en "Seleccionar archivo" y elegí el `.txt` o `.zip` exportado.
3. **Confirmar la carga:** La app mostrará la cantidad de mensajes detectados. Si el número es correcto, hacé clic en el botón para procesar.
4. **Explorar el dashboard:** Los resultados se muestran automáticamente con gráficos y métricas para cada análisis.
5. **Exportar a JSON:** Desde la interfaz se puede descargar el chat procesado en formato JSON.
6. **Resetear:** Para analizar otro chat, usá el botón de reset en la barra lateral.

---

## Testing

La estrategia de pruebas es manual y está documentada en planillas Excel dentro de cada categoría de `tests/`. Los casos de prueba cubren 10 áreas:

| Categoría | Qué se valida |
|-----------|---------------|
| Analíticas | Correctitud de cada métrica calculada |
| Calidad | Normalización de caracteres especiales, encodings |
| Formato | Aceptación/rechazo de tipos de archivo |
| Integrales | Flujo completo desde carga hasta visualización |
| Interfaz | Comportamiento y usabilidad de la UI |
| JSON | Estructura y contenido del archivo exportado |
| Rendimiento | Tiempo de respuesta con chats de gran tamaño |
| Resultados | Coherencia entre los datos del chat y lo mostrado |
| Seguridad | Resistencia ante archivos malformados o maliciosos |
| Subida | Manejo del componente de carga de archivos |

Para regenerar las planillas Excel de pruebas:

```bash
python tests/pruebas_calidad/generar_pruebas_calidad.py
python tests/pruebas_integrales/generar_pruebas_integrales.py
python tests/pruebas_rendimiento/generar_pruebas_rendimiento.py
python tests/pruebas_seguridad/generar_pruebas_seguridad.py
```

---

## Dependencias

| Librería | Propósito |
|----------|-----------|
| `streamlit` | Interfaz web interactiva sin frontend separado |
| `pandas` | Procesamiento y análisis de datos tabulares |
| `emoji` | Detección y normalización de emojis Unicode |
| `matplotlib` | Generación de gráficos de barras |
| `wordcloud` | Generación de la nube de palabras |
