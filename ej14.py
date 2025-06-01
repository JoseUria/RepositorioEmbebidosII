import cv2
import math

def read_and_show_image(path):
    img = cv2.imread(path)
    if img is None:
        print("Image not found.")
        exit()
    cv2.imshow("Original Image", img)
    cv2.waitKey(0)
    return img

def resize_image(img, width, height):
    resized = cv2.resize(img, (width, height))
    cv2.imshow(f"Resized Image ({width}x{height})", resized)
    cv2.waitKey(0)
    return resized

def split_into_n_quadrants(img, n):
    h, w = img.shape[:2]
    
    # Calcular la cantidad de filas y columnas necesarias
    rows = cols = int(math.sqrt(n))
    
    # Si n no es un cuadrado perfecto, ajustamos
    if rows * cols < n:
        cols += 1
    
    # Dividir la imagen en partes
    for i in range(rows):
        for j in range(cols):
            # Calcular las posiciones para el corte
            y_start = i * (h // rows)
            y_end = (i + 1) * (h // rows) if i < rows - 1 else h
            x_start = j * (w // cols)
            x_end = (j + 1) * (w // cols) if j < cols - 1 else w

            # Extraer el cuadrante
            quadrant = img[y_start:y_end, x_start:x_end]
            cv2.imshow(f"Quadrant {i*cols + j + 1}", quadrant)

    cv2.waitKey(0)

def split_horizontal(img):
    h = img.shape[0]
    top = img[:h//2, :]
    bottom = img[h//2:, :]
    cv2.imshow("Top Half", top)
    cv2.imshow("Bottom Half", bottom)
    cv2.waitKey(0)

def split_vertical(img):
    w = img.shape[1]
    left = img[:, :w//2]
    right = img[:, w//2:]
    cv2.imshow("Left Half", left)
    cv2.imshow("Right Half", right)
    cv2.waitKey(0)

def split_quadrants(img):
    h, w = img.shape[:2]
    q1 = img[:h//2, :w//2]   # top-left
    q2 = img[:h//2, w//2:]   # top-right
    q3 = img[h//2:, :w//2]   # bottom-left
    q4 = img[h//2:, w//2:]   # bottom-right

    cv2.imshow("Quadrant 1", q1)
    cv2.imshow("Quadrant 2", q2)
    cv2.imshow("Quadrant 3", q3)
    cv2.imshow("Quadrant 4", q4)
    cv2.waitKey(0)

if __name__ == "__main__":
    path = "/home/raspberry/lab7/gato.jpeg"
    image = read_and_show_image(path)

    resized = resize_image(image, 400, 600)

    # Solicitar al usuario el nmero de cuadrantes
    n = int(input("Enter the number of quadrants (ej 2x2): "))
    split_into_n_quadrants(resized, n)

    cv2.destroyAllWindows()
