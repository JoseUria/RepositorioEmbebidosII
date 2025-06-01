import cv2
import numpy as np
import threading

# Valores compartidos entre hilos
parametros = {
    "brillo": 0,
    "kernel_size": 3,
    "threshold1": 40,
    "threshold2": 160,
    "filtro": "gaussian",  # Filtro por defecto
    "ejecutar": True
}

def mostrar_menu():
    while parametros["ejecutar"]:
        print("\n--- CONSOLA DE AJUSTES ---")
        print(f"1. Brillo actual: {parametros['brillo']}")
        print(f"2. Kernel Size actual: {parametros['kernel_size']}")
        print(f"3. Threshold1 (bajo): {parametros['threshold1']}")
        print(f"4. Threshold2 (alto): {parametros['threshold2']}")
        print(f"5. Filtro actual: {parametros['filtro']}")
        print("6. Salir")

        opcion = input("Elige una opción (1-6): ")

        if opcion == "1":
            ajustar_brillo()
        elif opcion == "2":
            ajustar_kernel()
        elif opcion == "3":
            ajustar_threshold1()
        elif opcion == "4":
            ajustar_threshold2()
        elif opcion == "5":
            menu_filtros()
        elif opcion == "6":
            parametros["ejecutar"] = False
        else:
            print("Opción inválida.")

def menu_filtros():
    while True:
        print("\n--- MENÚ DE FILTROS ---")
        print("1. Media (Mean)")
        print("2. Bilateral")
        print("3. Gaussiano (Gaussian)")
        print("4. Mediana (Median)")
        print("5. Regresar al menú principal")
        
        opcion = input("Elige un filtro (1-5): ")
        
        if opcion == "1":
            parametros["filtro"] = "mean"
        elif opcion == "2":
            parametros["filtro"] = "bilateral"
        elif opcion == "3":
            parametros["filtro"] = "gaussian"
        elif opcion == "4":
            parametros["filtro"] = "median"
        elif opcion == "5":
            break
        else:
            print("Opción inválida.")

def ajustar_brillo():
    try:
        nuevo_brillo = int(input("Nuevo brillo (-100 a 100): "))
        parametros["brillo"] = np.clip(nuevo_brillo, -100, 100)
    except ValueError:
        print("Valor inválido.")

def ajustar_kernel():
    try:
        nuevo_kernel = int(input("Nuevo tamaño del kernel (impar > 1): "))
        if nuevo_kernel >= 3 and nuevo_kernel % 2 == 1:
            parametros["kernel_size"] = nuevo_kernel
        else:
            print("Debe ser un número impar mayor o igual a 3.")
    except ValueError:
        print("Valor inválido.")

def ajustar_threshold1():
    try:
        nuevo_t1 = int(input("Nuevo threshold1 (0-254): "))
        if 0 <= nuevo_t1 < parametros["threshold2"]:
            parametros["threshold1"] = nuevo_t1
        else:
            print("Debe ser menor que threshold2.")
    except ValueError:
        print("Valor inválido.")

def ajustar_threshold2():
    try:
        nuevo_t2 = int(input("Nuevo threshold2 (1-255): "))
        if parametros["threshold1"] < nuevo_t2 <= 255:
            parametros["threshold2"] = nuevo_t2
        else:
            print("Debe ser mayor que threshold1.")
    except ValueError:
        print("Valor inválido.")

def aplicar_filtro(filtro, imagen, kernel_size):
    if filtro == "mean":
        return cv2.blur(imagen, (kernel_size, kernel_size))  # Filtro de media
    elif filtro == "bilateral":
        return cv2.bilateralFilter(imagen, 9, 75, 75)  # Filtro bilateral
    elif filtro == "gaussian":
        return cv2.GaussianBlur(imagen, (kernel_size, kernel_size), 0)  # Filtro gaussiano
    elif filtro == "median":
        return cv2.medianBlur(imagen, kernel_size)  # Filtro de mediana
    else:
        return imagen

def procesar_canny_en_vivo(captura):
    while parametros["ejecutar"]:
        ret, frame = captura.read()
        if not ret:
            break

        ajustado = cv2.convertScaleAbs(frame, alpha=1, beta=parametros["brillo"])
        gris = cv2.cvtColor(ajustado, cv2.COLOR_BGR2GRAY)

        # Aplicar filtro según la opción seleccionada
        blur = aplicar_filtro(parametros["filtro"], gris, parametros["kernel_size"])

        bordes = cv2.Canny(blur, parametros["threshold1"], parametros["threshold2"])

        cv2.imshow("Canny en Tiempo Real", bordes)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            parametros["ejecutar"] = False
            break

    cv2.destroyAllWindows()

def main():
    url = "http://192.168.1.2:4747/video"  # Reemplaza con la IP correcta si es necesario
    captura = cv2.VideoCapture(url)

    if not captura.isOpened():
        print("Error al conectar con la cámara.")
        return

    hilo_menu = threading.Thread(target=mostrar_menu)
    hilo_menu.start()

    procesar_canny_en_vivo(captura)

    hilo_menu.join()
    captura.release()

if __name__ == "__main__":
    main()
