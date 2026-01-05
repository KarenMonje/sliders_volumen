# Control de Volumen con ArUco

Este proyecto permite controlar el volumen de Windows utilizando marcadores ArUco y una cámara web.

## Instalación y Configuración
1. **Crear y activar entorno virtual:**
   ```bash
   python -m venv clase 
   .\clase\Scripts\activate

2. **Instalar dependencias necesarias**
    pip install opencv-python opencv-contrib-python pycaw comtypes numpy

## Modo de uso
1. **Generar marcadores**
    python generate_aruco.py

2. **Ejecutar el marcador**
    python search_aruco.py
