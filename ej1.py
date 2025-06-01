import cv2

def cargar_video(ruta):
    return cv2.VideoCapture(ruta)

def crear_subtractores():
    fgbg_mog2 = cv2.createBackgroundSubtractorMOG2()
    fgbg_knn = cv2.createBackgroundSubtractorKNN()
    return fgbg_mog2, fgbg_knn

def mostrar_video(cap, fgbg_mog2, fgbg_knn):
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Aplicar sustraccin de fondo MOG2
        fgmask_mog2 = fgbg_mog2.apply(frame)

        # Aplicar sustraccin de fondo KNN
        fgmask_knn = fgbg_knn.apply(frame)

        # Mostrar los resultados
        cv2.imshow('Video Original', frame)
        cv2.imshow('MOG2 - Fondo Quitado', fgmask_mog2)
        cv2.imshow('KNN - Fondo Quitado', fgmask_knn)

        if cv2.waitKey(30) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    cap = cargar_video('/home/raspberry/lab9/bouncing.mp4.mp4')
    fgbg_mog2, fgbg_knn = crear_subtractores()
    mostrar_video(cap, fgbg_mog2, fgbg_knn)

main()
