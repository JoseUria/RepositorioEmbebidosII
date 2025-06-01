import tkinter as tk
from tkinter import ttk
from config_manager import parametros

def iniciar_gui():
    root = tk.Tk()
    root.title("Panel de Ajustes")

    def actualizar_valor(clave, var):
        parametros[clave] = var.get()

    def actualizar_hsv(indice, var):
        hsv_actual = list(parametros["hsv"][parametros["color_seleccionado"]][0 if indice < 3 else 1])
        hsv_actual[indice % 3] = var.get()
        if indice < 3:
            parametros["hsv"][parametros["color_seleccionado"]] = (tuple(hsv_actual), parametros["hsv"][parametros["color_seleccionado"]][1])
        else:
            parametros["hsv"][parametros["color_seleccionado"]] = (parametros["hsv"][parametros["color_seleccionado"]][0], tuple(hsv_actual))

    sliders = {
        "Brillo": ("brillo", -100, 100),
        "Kernel Size": ("kernel_size", 3, 31),
        "Threshold1": ("threshold1", 0, 254),
        "Threshold2": ("threshold2", 1, 255)
    }

    for texto, (clave, minimo, maximo) in sliders.items():
        tk.Label(root, text=texto).pack()
        var = tk.Scale(root, from_=minimo, to=maximo, orient=tk.HORIZONTAL)
        var.set(parametros[clave])
        var.config(command=lambda v, c=clave, vv=var: actualizar_valor(c, vv))
        var.pack()

    tk.Label(root, text="Filtro").pack()
    filtro = ttk.Combobox(root, values=["Gaussian", "Median", "Bilateral", "Mean"])
    filtro.set(parametros["filtro"])
    filtro.bind("<<ComboboxSelected>>", lambda e: parametros.update({"filtro": filtro.get()}))
    filtro.pack()

    tk.Label(root, text="Color HSV").pack()
    color = ttk.Combobox(root, values=["rojo", "verde", "amarillo", "azul"])
    color.set(parametros["color_seleccionado"])
    def cambiar_color(e):
        parametros["color_seleccionado"] = color.get()
        actualizar_sliders_hsv()
    color.bind("<<ComboboxSelected>>", cambiar_color)
    color.pack()

    tk.Checkbutton(root, text="Mostrar Canny", variable=tk.BooleanVar(value=parametros["mostrar_canny"]),
                   command=lambda: parametros.update({"mostrar_canny": not parametros["mostrar_canny"]})).pack()
    tk.Checkbutton(root, text="Mostrar HSV", variable=tk.BooleanVar(value=parametros["mostrar_hsv"]),
                   command=lambda: parametros.update({"mostrar_hsv": not parametros["mostrar_hsv"]})).pack()

    etiquetas = ["Hmin", "Smin", "Vmin", "Hmax", "Smax", "Vmax"]
    hsv_sliders = []

    def actualizar_sliders_hsv():
        color_act = parametros["color_seleccionado"]
        valores = list(parametros["hsv"][color_act][0]) + list(parametros["hsv"][color_act][1])
        for i, slider in enumerate(hsv_sliders):
            slider.set(valores[i])

    for i, nombre in enumerate(etiquetas):
        tk.Label(root, text=nombre).pack()
        slider = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, command=lambda v, idx=i: actualizar_hsv(idx, hsv_sliders[idx]))
        slider.pack()
        hsv_sliders.append(slider)

    actualizar_sliders_hsv()

    root.mainloop()
    parametros["ejecutar"] = False

