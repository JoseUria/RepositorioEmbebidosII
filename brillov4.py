import cv2
import numpy as np
import threading
import tkinter as tk
from tkinter import ttk

# Diccionario de parametros compartidos
parametros = {
    "brillo": 0,
    "kernel_size": 3,
    "threshold1": 40,
    "threshold2": 160,
    "filtro": "Gaussian",
    "mostrar_canny": True,
    "mostrar_hsv": False,
    "color_seleccionado": "rojo",
    "ejecutar": True,
    "hsv": {
        "rojo": [(0, 100, 100), (10, 255, 255)],
        "verde": [(40, 70, 70), (80, 255, 255)],
        "amarillo": [(20, 100, 100), (30, 255, 255)],
        "azul": [(100, 150, 0), (140, 255, 255)]
    }
}

# Aplicar el filtro seleccionado
def aplicar_filtro(imagen):
    if parametros["filtro"] == "Gaussian":
        return cv2.GaussianBlur(imagen, (parametros["kernel_size"], parametros["kernel_size"]), 0)
    elif parametros["filtro"] == "Median":
        return cv2.medianBlur(imagen, parametros["kernel_size"])
    elif parametros["filtro"] == "Bilateral":
        return cv2.bilateralFilter(imagen, 9, 75, 75)
    elif parametros["filtro"] == "Mean":
        return cv2.blur(imagen, (parametros["kernel_size"], parametros["kernel_size"]))
    return imagen

# Procesamiento de video
def procesar_video(captura):
    while parametros["ejecutar"]:
        ret, frame = captura.read()
        if not ret:
            break

        ajustado = cv2.convertScaleAbs(frame, alpha=1, beta=parametros["brillo"])

        if parametros["mostrar_canny"]:
            gris = cv2.cvtColor(ajustado, cv2.COLOR_BGR2GRAY)
            filtrado = aplicar_filtro(gris)
            bordes = cv2.Canny(filtrado, parametros["threshold1"], parametros["threshold2"])
            cv2.imshow("Canny", bordes)

        if parametros["mostrar_hsv"]:
            hsv = cv2.cvtColor(ajustado, cv2.COLOR_BGR2HSV)
            color = parametros["color_seleccionado"]
            rango_bajo, rango_alto = parametros["hsv"][color]
            mascara = cv2.inRange(hsv, np.array(rango_bajo), np.array(rango_alto))
            resultado = cv2.bitwise_and(ajustado, ajustado, mask=mascara)
            cv2.imshow("HSV", resultado)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            parametros["ejecutar"] = False
            break

    captura.release()
    cv2.destroyAllWindows()

# Interfaz grafica
def iniciar_gui():
    root = tk.Tk()
    root.title("Panel de Ajustes")

    def actualizar_valor(clave, var):
        parametros[clave] = var.get()

    def actualizar_hsv(index, canal, var):
        color = parametros["color_seleccionado"]
        nuevo = list(parametros["hsv"][color][index])
        nuevo[canal] = int(var.get())
        if index == 0:
            parametros["hsv"][color] = (tuple(nuevo), parametros["hsv"][color][1])
        else:
            parametros["hsv"][color] = (parametros["hsv"][color][0], tuple(nuevo))

    # Brillo
    tk.Label(root, text="Brillo").pack()
    s_brillo = tk.Scale(root, from_=-100, to=100, orient=tk.HORIZONTAL,
                        command=lambda v: actualizar_valor("brillo", s_brillo))
    s_brillo.set(parametros["brillo"])
    s_brillo.pack()

    # Kernel Size
    tk.Label(root, text="Kernel Size").pack()
    s_kernel = tk.Scale(root, from_=3, to=31, resolution=2, orient=tk.HORIZONTAL,
                        command=lambda v: actualizar_valor("kernel_size", s_kernel))
    s_kernel.set(parametros["kernel_size"])
    s_kernel.pack()

    # Thresholds
    tk.Label(root, text="Threshold1").pack()
    s_th1 = tk.Scale(root, from_=0, to=254, orient=tk.HORIZONTAL,
                     command=lambda v: actualizar_valor("threshold1", s_th1))
    s_th1.set(parametros["threshold1"])
    s_th1.pack()

    tk.Label(root, text="Threshold2").pack()
    s_th2 = tk.Scale(root, from_=1, to=255, orient=tk.HORIZONTAL,
                     command=lambda v: actualizar_valor("threshold2", s_th2))
    s_th2.set(parametros["threshold2"])
    s_th2.pack()

    # Filtro
    tk.Label(root, text="Filtro").pack()
    filtro = ttk.Combobox(root, values=["Gaussian", "Median", "Bilateral", "Mean"])
    filtro.set(parametros["filtro"])
    filtro.bind("<<ComboboxSelected>>", lambda e: actualizar_valor("filtro", filtro))
    filtro.pack()

    # Color HSV
    tk.Label(root, text="Color HSV").pack()
    color_cb = ttk.Combobox(root, values=["rojo", "verde", "amarillo", "azul"])
    color_cb.set(parametros["color_seleccionado"])
    color_cb.pack()

    sliders = []

    def actualizar_sliders():
        for s in sliders:
            s.destroy()
        sliders.clear()
        color = color_cb.get()
        parametros["color_seleccionado"] = color
        for i, nombre in enumerate(["H", "S", "V"]):
            for j in [0, 1]:
                tk.Label(root, text=f"{nombre} {'bajo' if j == 0 else 'alto'}").pack()
                val = parametros["hsv"][color][j][i]
                slider = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL)
                slider.set(val)
                slider.config(command=lambda v, idx=j, ch=i, s=slider: actualizar_hsv(idx, ch, s))
                slider.pack()
                sliders.append(slider)

    color_cb.bind("<<ComboboxSelected>>", lambda e: actualizar_sliders())
    actualizar_sliders()

    # Checks
    var_canny = tk.BooleanVar(value=parametros["mostrar_canny"])
    tk.Checkbutton(root, text="Mostrar Canny", variable=var_canny,
                   command=lambda: parametros.update({"mostrar_canny": var_canny.get()})).pack()

    var_hsv = tk.BooleanVar(value=parametros["mostrar_hsv"])
    tk.Checkbutton(root, text="Mostrar HSV", variable=var_hsv,
                   command=lambda: parametros.update({"mostrar_hsv": var_hsv.get()})).pack()

    root.mainloop()
    parametros["ejecutar"] = False

# Funcion principal
def main():
    url = "http://192.168.1.2:4747/video"  # Cambia la IP si es necesario
    captura = cv2.VideoCapture(url)
    if not captura.isOpened():
        print("Error al conectar con la camara")
        return

    hilo_video = threading.Thread(target=procesar_video, args=(captura,))
    hilo_video.start()

    iniciar_gui()
    hilo_video.join()

if __name__ == "__main__":
    main()
