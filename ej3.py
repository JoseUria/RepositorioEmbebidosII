import cv2

def cargar_video(ruta):
    return cv2.VideoCapture(ruta)

def crear_subtractores():
    fgbg_mog2 = cv2.createBackgroundSubtractorMOG2()
    fgbg_knn = cv2.createBackgroundSubtractorKNN()
    return fgbg_mog2, fgbg_knn

def mostrar_video(cap):
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convertir a escala de grises
        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Aplicar deteccin de bordes con Canny
        bordes = cv2.Canny(gris, 100, 200)

        # Mostrar los resultados
        #cv2.imshow('Video Original', frame)
        cv2.imshow('Canny - Bordes Detectados', bordes)

        if cv2.waitKey(30) & 0xFF == 27:  # Tecla ESC
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    cap = cargar_video('/home/raspberry/lab9/bouncing.mp4.mp4')
    mostrar_video(cap)

main()
