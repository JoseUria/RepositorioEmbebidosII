# main.py
import cv2
from camara import CamaraIP
from color import convertir_a_hsv, DetectorRojo, DetectorAzul, DetectorVerde

def main():
    camara = CamaraIP("http://172.20.10.4:4747/video")
    camara.abrir()

    try:
        while True:
            frame = camara.leer_frame()
            if frame is None:
                continue

            hsv = convertir_a_hsv(frame)

            rojo = DetectorRojo(hsv).detectar()
            azul = DetectorAzul(hsv).detectar()
            verde = DetectorVerde(hsv).detectar()

            cv2.imshow("Original", frame)
            cv2.imshow("Rojo", cv2.bitwise_and(frame, frame, mask=rojo))
            cv2.imshow("Azul", cv2.bitwise_and(frame, frame, mask=azul))
            cv2.imshow("Verde", cv2.bitwise_and(frame, frame, mask=verde))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        camara.cerrar()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
