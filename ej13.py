import cv2

def rotate_90(img):
    return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

if __name__ == "__main__":
    img = cv2.imread("/home/raspberry/lab7/gato.jpeg")

    if img is None:
        print("Image not found.")
        exit()

    while True:
        cv2.imshow("Rotating Image", img)
        key = cv2.waitKey(0)  
        if key == 27:  
            break
        img = rotate_90(img)  

    cv2.destroyAllWindows()
