import json
import os

ruta_config = "/home/raspberry/miniproyectoauto/config.json"

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

def guardar_configuracion():
    os.makedirs(os.path.dirname(ruta_config), exist_ok=True)
    with open(ruta_config, 'w') as archivo:
        json.dump(parametros, archivo, indent=4)
