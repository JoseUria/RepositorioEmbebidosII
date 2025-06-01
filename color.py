# color.py
import cv2
import numpy as np

class DetectorColorBase:
    def __init__(self, hsv: np.ndarray):
        self.hsv = hsv

    def crear_mascara(self, bajo, alto):
        return cv2.inRange(self.hsv, np.array(bajo), np.array(alto))

    def detectar(self):
        raise NotImplementedError("Implementar en subclase")


class DetectorRojo(DetectorColorBase):
    def detectar(self):
        m1 = self.crear_mascara([0, 100, 100], [10, 255, 255])
        m2 = self.crear_mascara([160, 100, 100], [180, 255, 255])
        return cv2.bitwise_or(m1, m2)


class DetectorAzul(DetectorColorBase):
    def detectar(self):
        return self.crear_mascara([100, 150, 0], [140, 255, 255])


class DetectorVerde(DetectorColorBase):
    def detectar(self):
        return self.crear_mascara([40, 100, 100], [80, 255, 255])


def convertir_a_hsv(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
