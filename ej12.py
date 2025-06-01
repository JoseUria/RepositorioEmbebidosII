import cv2

def resize_image(img, option):
    #toma las primeras caracteristicas
    height, width = img.shape[:2]

    if option == "original":
        return img
    elif option == "small":
        scale = 0.25
    elif option == "medium":
        scale = 0.5
    elif option == "big":
        scale = 1.5
    else:
        print("Invalid option. Showing original image.")
        return img

    new_size = (int(width * scale), int(height * scale))
    return cv2.resize(img, new_size)

if __name__ == "__main__":
    img = cv2.imread("/home/raspberry/lab7/gato.jpeg")

    if img is None:
        print("Image not found.")
        exit()

    print("Choose image size:")
    print("Options: original, small, medium, big")
    #strip quita espacios y lower pone todo en minusculas
    choice = input("Enter your choice: ").strip().lower()

    resized = resize_image(img, choice)
    cv2.imshow(f"{choice} image", resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
