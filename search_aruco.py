#Se utiliza la proyeccion escalar para calcular la posicion del controlador sobre la barra en vez 
# de la formula de el valor medio entre dos puntos, ya que esta es mas precisa y 
# asi se evita problemas con el volumen cuando los arucos no estan alineados horizontalmente o en algun otro lugar.

import cv2
import cv2.aruco as aruco
import numpy as np
import math
# Librerías para controlar el volumen en Windows
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import ctypes

class Slider:
    def __init__(self, diccionario_aruco, parametros):
        # Guardar el diccionario y parámetros que usamos para detectar
        self.diccionario_aruco = diccionario_aruco
        self.parametros = parametros
        
        # Configurar el control de volumen del sistema
        dispositivos = AudioUtilities.GetSpeakers()
        interfaz = dispositivos.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volumen = ctypes.cast(interfaz, ctypes.POINTER(IAudioEndpointVolume))
    
    def procesar_frame(self, frame):

        # Convertir a gris porque así se detectan mejor los ArUcos
        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detectar los marcadores ArUco en la imagen
        esquinas, ids, rechazados = aruco.detectMarkers(gris, self.diccionario_aruco, parameters=self.parametros)
        
        # Si encontramos al menos un ArUco
        if ids is not None:
            # Dibujar los contornos de los ArUcos detectados
            aruco.drawDetectedMarkers(frame, esquinas, ids)
            
            # Diccionario para guardar el centro de cada ArUco según su ID
            centros = {}
            
            # Recorrer cada ArUco encontrado
            for i in range(len(esquinas)):
                esquina = esquinas[i]
                id_aruco = ids[i][0]
                # Calcular el centro promediando todas las esquinas
                x_centro = int(sum([p[0] for p in esquina[0]]) / 4)
                y_centro = int(sum([p[1] for p in esquina[0]]) / 4)
                
                centros[id_aruco] = (x_centro, y_centro)

            # Verificar que tenemos los 3 ArUcos necesarios
            if len(centros) == 3:
                # Obtener las coordenadas de cada punto
                # volumen bajo
                x1, y1 = centros[0]
                # volumen alto
                x2, y2 = centros[1]
                # controlador
                xc, yc = centros[2]
                
                # Dibujar la linea azul entre los dos volumenes
                cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
                
                # Vector de la barra (del 0 al 1)
                vector_barra_x = x2 - x1
                vector_barra_y = y2 - y1
                vector_barra = np.array([vector_barra_x, vector_barra_y], float)
                
                # Vector desde el 0 hasta el controlador
                vector_controlador_x = xc - x1
                vector_controlador_y = yc - y1
                vector_controlador = np.array([vector_controlador_x, vector_controlador_y], float)

                # Producto punto para proyectar el controlador sobre la barra, esto nos dice qué tan lejos está sobre la línea
                producto_punto = np.dot(vector_controlador, vector_barra)
                longitud_barra = np.dot(vector_barra, vector_barra)
                
                # t es la posición en pixeles a porcentaje (0.0 a 1.0)
                t = producto_punto / longitud_barra
                
                # debe estar entre 0 y 1
                if t < 0.0:
                    t = 0.0
                elif t > 1.0:
                    t = 1.0
                
                # Calcular el punto ubicado sobre la barra
                x_ubicar = int(x1 + t * vector_barra_x)
                y_ubicar = int(y1 + t * vector_barra_y)
                
                # punto rojo donde se ubica el controlador
                cv2.circle(frame, (x_ubicar, y_ubicar), 8, (0, 0, 255), -1)

                # linea amarilla desde el controlador hasta su proyección
                cv2.line(frame, (xc, yc), (x_ubicar, y_ubicar), (0, 255, 255), 2)

                # Mostrar el porcentaje de volumen
                porcentaje_volumen = int(t * 100)
                cv2.putText(frame, f"Vol: {porcentaje_volumen}%",
                           (x_ubicar + 10, y_ubicar),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                
                # volumen del sistema (0.0 = mínimo, 1.0 = máximo)
                self.volumen.SetMasterVolumeLevelScalar(t, None)
        
        return frame

# Elegir el mismo diccionario que usaste para generar los ArUcos
diccionario_aruco = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parametros = aruco.DetectorParameters()

# Crear slider
slider = Slider(diccionario_aruco, parametros)

captura = cv2.VideoCapture(0)

print("Presiona 'x' para salir")


while True:
    ret, frame = captura.read()
    
    if not ret:
        print("No se pudo acceder a la cámara")
        break
    
    frame = slider.procesar_frame(frame)
    
    cv2.imshow("Control de Volumen con ArUcos", frame)
    
    # Para salir la x
    tecla = cv2.waitKey(1) & 0xFF
    if tecla == ord('x'):
        break

# Cerrar todo
captura.release()
cv2.destroyAllWindows()
print("Programa terminado")