import cv2
import numpy as np

def analyze_color_content(img_path):
    img = cv2.imread(img_path)
    if img is None:
        print(f"Error loading {img_path}")
        return None
    blue_channel = img[:, :, 0]
    green_channel = img[:, :, 1]
    red_channel = img[:, :, 2]


    avg_blue = np.mean(blue_channel)
    avg_green = np.mean(green_channel)
    avg_red = np.mean(red_channel)

    print(f"Image: {img_path}")
    print(f"Average Blue: {avg_blue:.2f}")
    print(f"Average Green: {avg_green:.2f}")
    print(f"Average Red: {avg_red:.2f}")

    return img

def rgb_to_grayscale(img):
  
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray

if __name__ == "__main__":
    path = "/home/raspberry/lab7/gato.jpeg"
    img = analyze_color_content(path)
    if img is not None:
        gray_img = rgb_to_grayscale(img)

        cv2.imshow("Original", img)
        cv2.imshow("Grayscale", gray_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
