import cv2
import numpy as np

class ImageColorConverter:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise FileNotFoundError(f"Error loading {image_path}")
    
    def to_rgb(self):
        rgb_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        cv2.imshow("RGB Image", rgb_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def to_grayscale(self):
        gray_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Grayscale Image", gray_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def to_hsv(self):
        hsv_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        cv2.imshow("HSV Image", hsv_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    path = "/home/raspberry/lab7/gato.jpeg"
    converter = ImageColorConverter(path)

 
    converter.to_rgb()

  
    converter.to_grayscale()

   
    converter.to_hsv()
