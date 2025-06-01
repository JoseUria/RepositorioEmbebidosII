# camara.py
import cv2

class CamaraBase:
    def abrir(self):
        raise NotImplementedError

    def leer_frame(self):
        raise NotImplementedError

    def cerrar(self):
        raise NotImplementedError


class CamaraIP(CamaraBase):
    def __init__(self, url):
        self.url = url
        self.cap = None

    def abrir(self):
        self.cap = cv2.VideoCapture(self.url)
        if not self.cap.isOpened():
            raise Exception("No se pudo abrir la camara IP.")

    def leer_frame(self):
        ret, frame = self.cap.read()
        return frame if ret else None

    def cerrar(self):
        if self.cap:
            self.cap.release()
