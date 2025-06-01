import cv2
import numpy as np
import threading

# Valores iniciales para los parámetros
parametros = {
    "brillo": 0,
    "kernel_size": 3,
    "threshold1": 40,
    "threshold2": 160,
    "filtro": "gaussian",  # Filtro por defecto
    "ejecutar": True
}

def crear_barras_interactivas():
    # Crear una ventana para los sliders
    cv2.namedWindow("Ajustes Interactivos")

    # Barras de ajuste de brillo
    cv2.createTrackbar("Brillo", "Ajustes Interactivos", 100, 200, lambda x: None)  # rango de -100 a 100

    # Barras de ajuste de kernel size
    cv2.createTrackbar("Kernel Size", "Ajustes Interactivos", 3, 21, lambda x: None)  # rango de 3 a 21 (impar)

    # Barras de ajuste de thresholds
    cv2.createTrackbar("Threshold1", "Ajustes Interactivos", 40, 255, lambda x: None)  # rango de 0 a 255
    cv2.createTrackbar("Threshold2", "Ajustes Interactivos", 160, 255, lambda x: None)  # rango de 0 a 255

    # Barras de ajuste de filtros (usamos una barra para elegir entre filtros)
    cv2.createTrackbar("Filtro", "Ajustes Interactivos", 1, 4, lambda x: None)  # 1: Mean, 2: Bilateral, 3: Gaussian, 4: Median

def obtener_valores_barras():
    # Obtener valores de los sliders
    brillo = cv2.getTrackbarPos("Brillo", "Ajustes Interactivos") - 100
    kernel_size = cv2.getTrackbarPos("Kernel Size", "Ajustes Interactivos") | 1  # Asegura que sea impar
    threshold1 = cv2.getTrackbarPos("Threshold1", "Ajustes Interactivos")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Ajustes Interactivos")
    filtro = cv2.getTrackbarPos("Filtro", "Ajustes Interactivos")

    return brillo, kernel_size, threshold1, threshold2, filtro

def menu_filtros(filtro):
    # Mapeamos el valor del filtro a un string
    if filtro == 1:
        return "mean"
    elif filtro == 2:
        return "bilateral"
    elif filtro == 3:
        return "gaussian"
    elif filtro == 4:
        return "median"
    else:
        return "gaussian"  # Valor predeterminado

def aplicar_filtro(filtro, imagen, kernel_size):
    if filtro == "mean":
        return cv2.blur(imagen, (kernel_size, kernel_size))  # Filtro de media
    elif filtro == "bilateral":
        return cv2.bilateralFilter(imagen, 9, 75, 75)  # Filtro bilateral
    elif filtro == "gaussian":
        return cv2.GaussianBlur(imagen, (kernel_size, kernel_size), 0)  # Filtro gaussiano
    elif filtro == "median":
        return cv2.medianBlur(imagen, kernel_size)  # Filtro de mediana
    else:
        return imagen

def procesar_canny_en_vivo(captura):
    while parametros["ejecutar"]:
        ret, frame = captura.read()
        if not ret:
            break

        brillo, kernel_size, threshold1, threshold2, filtro = obtener_valores_barras()

        ajustado = cv2.convertScaleAbs(frame, alpha=1, beta=brillo)
        gris = cv2.cvtColor(ajustado, cv2.COLOR_BGR2GRAY)

        # Aplicar filtro según la opción seleccionada
        blur = aplicar_filtro(menu_filtros(filtro), gris, kernel_size)

        bordes = cv2.Canny(blur, threshold1, threshold2)

        cv2.imshow("Canny en Tiempo Real", bordes)

        # Salir si presionas 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            parametros["ejecutar"] = False
            break

    cv2.destroyAllWindows()

def main():
    url = "http://192.168.1.2:4747/video"  # Reemplaza con la IP correcta si es necesario
    captura = cv2.VideoCapture(url)

    if not captura.isOpened():
        print("Error al conectar con la cámara.")
        return

    # Crear la ventana interactiva para los sliders
    crear_barras_interactivas()

    procesar_canny_en_vivo(captura)

    captura.release()

if __name__ == "__main__":
    main()
