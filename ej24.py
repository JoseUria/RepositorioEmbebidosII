import cv2
import numpy as np

def detect_color(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("Error al cargar la imagen.")
        return

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

   
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([179, 255, 255])

  
    lower_green = np.array([40, 100, 100])
    upper_green = np.array([70, 255, 255])

    
    lower_blue = np.array([100, 100, 100])
    upper_blue = np.array([130, 255, 255])

   
    red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = red_mask1 + red_mask2

    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

   
    if np.any(red_mask):
        print("? Rojo detectado")
    if np.any(green_mask):
        print("? Verde detectado")
    if np.any(blue_mask):
        print("? Azul detectado")

    cv2.imshow("Original", img)
    cv2.imshow("Red Mask", red_mask)
    cv2.imshow("Green Mask", green_mask)
    cv2.imshow("Blue Mask", blue_mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_color("/home/raspberry/lab7/gato.jpeg")
