# TP Ingeniería de Software III - Entregable 1

Esta es la guía rápida de configuración y ejecución del proyecto para facilitar el testeo y evaluación de este primer entregable.

## Requisitos Previos
-   Tener instalado Python (recomendado 3.8 o superior).

## Pasos para la Ejecución
1.  Navegar a la raíz del proyecto:  
    Asegúrate de estar posicionado en la carpeta principal del repositorio (tp-ing-soft-iii).
    
2.  Crear un entorno virtual (recomendado):  
    Para no generar conflictos con las dependencias globales, crea un entorno virtual llamado venv:  
    python -m venv venv
    
3.  Activar el entorno virtual:
-   En Windows:  
    venv\Scripts\activate
-   En macOS/Linux:  
    source venv/bin/activate
    
4.  Instalar las dependencias:  
    Con el entorno virtual activado, instala Streamlit y demás librerías requeridas utilizando el archivo requirements.txt:  
    pip install -r requirements.txt
    

5.  Ejecutar la aplicación Streamlit:  
Levanta el servidor local ejecutando el archivo principal de la interfaz:  
streamlit run app.py  
Esto debería abrir automáticamente una pestaña en el navegador web (usualmente en http://localhost:8501).