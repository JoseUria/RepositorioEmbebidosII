import tkinter as tk
from tkinter import ttk
import json
from config import parametros

class GUIController:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Panel de Control - Ajustes de Video")
        self.crear_widgets()

    def crear_slider(self, etiqueta, variable, desde, hasta, fila):
        tk.Label(self.root, text=etiqueta).grid(row=fila, column=0)
        slider = tk.Scale(self.root, from_=desde, to=hasta, orient=tk.HORIZONTAL,
                          command=lambda val: parametros.update({variable: int(val)}))
        slider.set(parametros[variable])
        slider.grid(row=fila, column=1, padx=10, pady=5)

    def crear_widgets(self):
        self.crear_slider("Brillo", "brillo", -100, 100, 0)
        self.crear_slider("Kernel", "kernel_size", 1, 15, 1)
        self.crear_slider("Umbral 1", "threshold1", 0, 255, 2)
        self.crear_slider("Umbral 2", "threshold2", 0, 255, 3)

        # Menu desplegable para tipo de filtro
        tk.Label(self.root, text="Filtro").grid(row=4, column=0)
        opciones = ["Gaussian", "Median", "Bilateral", "Mean"]
        filtro_menu = ttk.Combobox(self.root, values=opciones, state="readonly")
        filtro_menu.set(parametros["filtro"])
        filtro_menu.grid(row=4, column=1)
        filtro_menu.bind("<<ComboboxSelected>>", lambda e: parametros.update({"filtro": filtro_menu.get()}))

        # Botones de mostrar Canny y HSV
        tk.Checkbutton(self.root, text="Mostrar Canny",
                       variable=tk.BooleanVar(value=parametros["mostrar_canny"]),
                       command=lambda: parametros.update({"mostrar_canny": not parametros["mostrar_canny"]})
                       ).grid(row=5, column=0, columnspan=2)

        tk.Checkbutton(self.root, text="Mostrar HSV",
                       variable=tk.BooleanVar(value=parametros["mostrar_hsv"]),
                       command=lambda: parametros.update({"mostrar_hsv": not parametros["mostrar_hsv"]})
                       ).grid(row=6, column=0, columnspan=2)

        # Seleccion de color a seguir
        tk.Label(self.root, text="Color a seguir").grid(row=7, column=0)
        colores = ["rojo", "verde", "amarillo", "azul"]
        color_menu = ttk.Combobox(self.root, values=colores, state="readonly")
        color_menu.set(parametros["color_seleccionado"])
        color_menu.grid(row=7, column=1)
        color_menu.bind("<<ComboboxSelected>>", lambda e: parametros.update({"color_seleccionado": color_menu.get()}))

        # Boton para guardar configuracion
        tk.Button(self.root, text="Guardar Configuracion", command=self.guardar_config).grid(row=8, column=0, columnspan=2, pady=10)

        # Boton para cerrar
        tk.Button(self.root, text="Salir", command=self.cerrar).grid(row=9, column=0, columnspan=2, pady=10)

    def guardar_config(self):
        ruta = "/home/raspberry/miniproyectoauto/config.json"
        with open(ruta, "w") as archivo:
            json.dump(parametros, archivo, indent=4)
        print(f"Configuracion guardada en {ruta}")

    def cerrar(self):
        parametros["ejecutar"] = False
        self.root.quit()

    def iniciar(self):
        self.root.mainloop()


def iniciar_gui():
    app = GUIController()
    app.iniciar()
