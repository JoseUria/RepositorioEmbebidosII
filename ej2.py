import cv2
import threading

frame_actual = None
ret_actual = False
lock = threading.Lock()
ejecutando = True

def leer_frames(captura):
    global frame_actual, ret_actual, ejecutando
    while ejecutando:
        ret, frame = captura.read()
        with lock:
            ret_actual = ret
            frame_actual = frame

def abrir_captura(url):
    return cv2.VideoCapture(url)

def crear_subtractor():
    return cv2.createBackgroundSubtractorMOG2()

def detectar_objeto(fgmask, frame):
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    altura, ancho = frame.shape[:2]
    centro_x = ancho // 2
    centro_y = altura // 2

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            obj_centro_x = x + w // 2
            obj_centro_y = y + h // 2

            cv2.circle(frame, (obj_centro_x, obj_centro_y), 5, (0, 0, 255), -1)

            if abs(obj_centro_x - centro_x) < 30 and abs(obj_centro_y - centro_y) < 30:
                cv2.putText(frame, "Objeto en el centro!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                            1, (0, 0, 255), 2)

    cv2.circle(frame, (centro_x, centro_y), 10, (255, 0, 0), 2)

def mostrar_video(subtractor):
    global ejecutando
    while True:
        with lock:
            ret = ret_actual
            frame = frame_actual.copy() if frame_actual is not None else None

        if not ret or frame is None:
            continue

        fgmask = subtractor.apply(frame)
        detectar_objeto(fgmask, frame)

        cv2.imshow("USB DroidCam", frame)
        cv2.imshow("Mascara de fondo", fgmask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            ejecutando = False
            break

def cerrar_captura(captura):
    captura.release()
    cv2.destroyAllWindows()

def main():
    global ejecutando
    url = "http://192.168.1.3:4747/video"
    captura = abrir_captura(url)
    subtractor = crear_subtractor()

    hilo_lectura = threading.Thread(target=leer_frames, args=(captura,))
    hilo_lectura.start()

    mostrar_video(subtractor)

    ejecutando = False
    hilo_lectura.join()
    cerrar_captura(captura)

if __name__ == "__main__":
    main()
