import cv2

def detectar_formas(imagen, mascara, color):
    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contorno in contornos:
        area = cv2.contourArea(contorno)
        if area > 500:
            approx = cv2.approxPolyDP(contorno, 0.04 * cv2.arcLength(contorno, True), True)
            vertices = len(approx)
            forma = "Desconocida"
            if vertices == 3:
                forma = "Triangulo"
            elif vertices == 4:
                forma = "Cuadrado o Rectangulo"
            elif vertices > 4:
                forma = "Circulo"

            x, y, w, h = cv2.boundingRect(contorno)
            cv2.rectangle(imagen, (x, y), (x+w, y+h), (255, 255, 255), 2)
            cv2.putText(imagen, f"{forma} - {color}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
