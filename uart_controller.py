import serial
import time
import cv2

class UARTTracker:
    def __init__(self, port="/dev/ttyACM0", baud=115200):
        self.ser = serial.Serial(port, baud, timeout=1)
        time.sleep(2)

    def rastrear_rojo(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(hsv, (0, 100, 100), (10, 255, 255))
        mask2 = cv2.inRange(hsv, (160, 100, 100), (180, 255, 255))
        mask = cv2.bitwise_or(mask1, mask2)

        contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        objetos = [cnt for cnt in contornos if cv2.contourArea(cnt) > 500]

        if len(objetos) == 1:
            self.ser.write(b'1')
        elif len(objetos) >= 2:
            self.ser.write(b'2')
        else:
            self.ser.write(b'3')

        return mask
