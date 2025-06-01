import cv2
import numpy as np
import threading

# Valores compartidos entre hilos
parametros = {
    "brillo": 0,
    "kernel_size": 3,
    "threshold1": 40,
    "threshold2": 160,
    "color": "ninguno",
    "ejecutar": True
}

rangos_hsv = {
    "rojo": [(np.array([0, 100, 100]), np.array([10, 255, 255])), 
             (np.array([160, 100, 100]), np.array([179, 255, 255]))],  # Dos rangos por el hue circular
    "verde": [(np.array([40, 70, 70]), np.array([80, 255, 255]))],
    "azul": [(np.array([100, 150, 0]), np.array([140, 255, 255]))],
    "amarillo": [(np.array([20, 100, 100]), np.array([30, 255, 255]))]
}

def mostrar_menu():
    while parametros["ejecutar"]:
        print("\n--- CONSOLA DE AJUSTES ---")
        print(f"1. Brillo actual: {parametros['brillo']}")
        print(f"2. Kernel Size actual: {parametros['kernel_size']}")
        print(f"3. Threshold1 (bajo): {parametros['threshold1']}")
        print(f"4. Threshold2 (alto): {parametros['threshold2']}")
        print(f"5. Color HSV actual: {parametros['color']}")
        print("6. Salir")

        opcion = input("Elige una opcion (1-6): ")

        if opcion == "1":
            try:
                nuevo_brillo = int(input("Nuevo brillo (-100 a 100): "))
                parametros["brillo"] = np.clip(nuevo_brillo, -100, 100)
            except ValueError:
                print("Valor invalido.")
        elif opcion == "2":
            try:
                nuevo_kernel = int(input("Nuevo tamano del kernel (impar >= 3): "))
                if nuevo_kernel >= 3 and nuevo_kernel % 2 == 1:
                    parametros["kernel_size"] = nuevo_kernel
                else:
                    print("Debe ser un numero impar mayor o igual a 3.")
            except ValueError:
                print("Valor invalido.")
        elif opcion == "3":
            try:
                nuevo_t1 = int(input("Nuevo threshold1 (0-254): "))
                if 0 <= nuevo_t1 < parametros["threshold2"]:
                    parametros["threshold1"] = nuevo_t1
                else:
                    print("Debe ser menor que threshold2.")
            except ValueError:
                print("Valor invalido.")
        elif opcion == "4":
            try:
                nuevo_t2 = int(input("Nuevo threshold2 (1-255): "))
                if parametros["threshold1"] < nuevo_t2 <= 255:
                    parametros["threshold2"] = nuevo_t2
                else:
                    print("Debe ser mayor que threshold1.")
            except ValueError:
                print("Valor invalido.")
        elif opcion == "5":
            color = input("Elige un color (rojo, verde, azul, amarillo, ninguno): ").strip().lower()
            if color in rangos_hsv or color == "ninguno":
                parametros["color"] = color
            else:
                print("Color no valido.")
        elif opcion == "6":
            parametros["ejecutar"] = False
        else:
            print("Opcion invalida.")

def procesar_canny_en_vivo(captura):
    while parametros["ejecutar"]:
        ret, frame = captura.read()
        if not ret:
            break

        ajustado = cv2.convertScaleAbs(frame, alpha=1, beta=parametros["brillo"])

        # Procesamiento Canny
        gris = cv2.cvtColor(ajustado, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gris, (parametros["kernel_size"], parametros["kernel_size"]), 0)
        bordes = cv2.Canny(blur, parametros["threshold1"], parametros["threshold2"])
        cv2.imshow("Canny", bordes)

        # Deteccion de color HSV
        if parametros["color"] != "ninguno":
            hsv = cv2.cvtColor(ajustado, cv2.COLOR_BGR2HSV)
            mascara_total = None
            for (lower, upper) in rangos_hsv.get(parametros["color"], []):
                mascara = cv2.inRange(hsv, lower, upper)
                if mascara_total is None:
                    mascara_total = mascara
                else:
                    mascara_total = cv2.bitwise_or(mascara_total, mascara)
            resultado = cv2.bitwise_and(ajustado, ajustado, mask=mascara_total)
            cv2.imshow("Color Detectado", resultado)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            parametros["ejecutar"] = False
            break

    cv2.destroyAllWindows()

def main():
    url = "http://192.168.1.2:4747/video"  # Reemplaza con la IP correcta si es necesario
    captura = cv2.VideoCapture(url)

    if not captura.isOpened():
        print("Error al conectar con la camara.")
        return

    hilo_menu = threading.Thread(target=mostrar_menu)
    hilo_menu.start()

    procesar_canny_en_vivo(captura)

    hilo_menu.join()
    captura.release()

if __name__ == "__main__":
    main()
