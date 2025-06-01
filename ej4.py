import cv2
import numpy as np

# Ruta de la imagen
ruta_imagen = '/home/raspberry/lab9/monedas_2.jpg'

# Cargar imagen
imagen = cv2.imread(ruta_imagen)
if imagen is None:
    print("Error al cargar la imagen. Verifica la ruta.")
    exit()

# Preprocesamiento
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gris, (15, 15), 0)

# Binarizacin usando Canny para detectar bordes
bordes = cv2.Canny(blur, 40, 160)

# Encontrar contornos
contornos, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

contador_monedas = 0

for c in contornos:
    area = cv2.contourArea(c)
    # Filtrar contornos pequenos
    if area > 130:  
        #se usara una formula que me permitira encontrar la distancia entre contornos , en este caso usa 0.01 una distancia buena,entre mas grande menos util es
        epsilon = 0.01 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)
        #calcula los vertices de un cuadrado donde "x" y "y" son los vertices superior e inferior y los otros valores son al ancho del cuadro  
        x, y, w, h = cv2.boundingRect(approx)
        #los valores finales son el clor del cuadrado en este caso verde y el 2 del final es el grosor de la linea
        cv2.rectangle(imagen, (x, y), (x + w, y + h), (0, 255, 0), 2)
        contador_monedas += 1

print(f"Se detectaron {contador_monedas} monedas.")

# Mostrar resultados
cv2.imshow('Monedas detectadas', imagen)
cv2.imshow('Bordes', bordes)
cv2.waitKey(0)
cv2.destroyAllWindows()
