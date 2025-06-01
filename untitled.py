import cv2
import numpy as np

# Cargar el video
cap = cv2.VideoCapture('/home/raspberry/Downloads/WhatsApp Video 2025-04-28 at 15.48.05.mp4')  # Cambia 'tu_video.mp4' por tu archivo

if not cap.isOpened():
    print("Error al abrir el video.")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Redimensionar el video a (400, 600) (ancho, alto)
    frame_resized = cv2.resize(frame, (400, 600))

    # Deteccion de bordes usando Canny
    edges = cv2.Canny(frame_resized, 100, 200)

    # Dividir en dos mitades (vertical)
    height, width, _ = frame_resized.shape
    mitad_izquierda = frame_resized[:, :width//2]
    mitad_derecha = frame_resized[:, width//2:]

    # Dividir en cuatro cuadrantes
    cuadrante_1 = frame_resized[:height//2, :width//2]  # arriba izquierda
    cuadrante_2 = frame_resized[:height//2, width//2:]  # arriba derecha
    cuadrante_3 = frame_resized[height//2:, :width//2]  # abajo izquierda
    cuadrante_4 = frame_resized[height//2:, width//2:]  # abajo derecha

    # Mostrar los resultados
    cv2.imshow('Video Original Redimensionado', frame_resized)
    cv2.imshow('Deteccion de Bordes', edges)
    cv2.imshow('Mitad Izquierda', mitad_izquierda)
    cv2.imshow('Mitad Derecha', mitad_derecha)

    # Crear una ventana con los 4 cuadrantes combinados
    arriba = np.hstack((cuadrante_1, cuadrante_2))
    abajo = np.hstack((cuadrante_3, cuadrante_4))
    cuadrantes = np.vstack((arriba, abajo))

    cv2.imshow('Cuatro Cuadrantes', cuadrantes)

    # Salir cuando se presione 'q'
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()


