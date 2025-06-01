import cv2

def abrir_captura(url):
    return cv2.VideoCapture(url)

def mostrar_video(captura):
    while True:
        ret, frame = captura.read()
        if not ret:
            break
        cv2.imshow("USB DroidCam", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def cerrar_captura(captura):
    captura.release()
    cv2.destroyAllWindows()

def main():
    url = "http://192.168.43.1:4747/video"
    captura = abrir_captura(url)
    mostrar_video(captura)
    cerrar_captura(captura)

if __name__ == "__main__":
    main()
