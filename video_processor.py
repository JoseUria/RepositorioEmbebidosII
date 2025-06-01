import cv2
import numpy as np
from filtro_utils import aplicar_filtro, detectar_figuras_y_colores
from config_manager import parametros, guardar_configuracion

def procesar_video(captura):
    while parametros["ejecutar"]:
        ret, frame = captura.read()
        if not ret:
            break

        ajustado = cv2.convertScaleAbs(frame, alpha=1, beta=parametros["brillo"])

        if parametros["mostrar_canny"]:
            gris = cv2.cvtColor(ajustado, cv2.COLOR_BGR2GRAY)
            filtrado = aplicar_filtro(gris)
            bordes = cv2.Canny(filtrado, parametros["threshold1"], parametros["threshold2"])
            cv2.imshow("Canny", bordes)

        if parametros["mostrar_hsv"]:
            hsv = cv2.cvtColor(ajustado, cv2.COLOR_BGR2HSV)
            color = parametros["color_seleccionado"]
            rango_bajo, rango_alto = parametros["hsv"][color]
            mascara = cv2.inRange(hsv, np.array(rango_bajo), np.array(rango_alto))
            resultado = cv2.bitwise_and(ajustado, ajustado, mask=mascara)

            detectar_figuras_y_colores(resultado, mascara)
            cv2.imshow("HSV", resultado)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            parametros["ejecutar"] = False
            break

    captura.release()
    cv2.destroyAllWindows()
    guardar_configuracion()
