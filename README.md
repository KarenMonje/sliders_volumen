# Control de Volumen con ArUco

Este proyecto permite controlar el volumen de Windows utilizando marcadores ArUco y una cámara web.

## Instalación y Configuración
1. **Crear y activar entorno virtual:**
   ```bash
   python -m venv clase 
   .\clase\Scripts\activate

2. **Instalar dependencias necesarias**
   ```bash
    pip install opencv-python opencv-contrib-python pycaw comtypes numpy

## Modo de uso
1. **Generar marcadores**
   ```bash
    python generate_aruco.py

3. **Ejecutar el marcador**
   ```bash
    python search_aruco.py
