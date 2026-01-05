import cv2
import cv2.aruco as aruco

aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

# Tamaño en pixeles de cada marcador
marker_size = 200  

# Crear 3 marcadores distintos
for i in range(3):
    # Generar el marcador con ID = i
    marker_image = aruco.generateImageMarker(aruco_dict, i, marker_size)

    # Guardar la imagen en disco
    filename = f"aruco_{i}.png"
    cv2.imwrite(filename, marker_image)
    print(f"Guardado: {filename}")

print("✅ Listo. Se crearon 3 ArUcos (IDs 0, 1 y 2).")