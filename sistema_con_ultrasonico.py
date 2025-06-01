import cv2
import numpy as np
import threading
import tkinter as tk
from tkinter import ttk
import json
import os
import serial
import time
import RPi.GPIO as GPIO

ruta_config = "/home/raspberry/miniproyectoauto/config.json"
UART_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200

# Inicializa UART
ser = serial.Serial(UART_PORT, BAUD_RATE, timeout=1)
time.sleep(2)

# Pines del sensor ultrasónico
TRIG = 23
ECHO = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

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

ultimo_estado_uart = None
modo_bloqueado = False

def medir_distancia():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    duracion = pulse_end - pulse_start
    distancia = duracion * 17150
    return round(distancia, 2)

def control_ultrasonico():
    global modo_bloqueado
    while parametros["ejecutar"]:
        distancia = medir_distancia()
        if distancia < 10:
            if not modo_bloqueado:
                ser.write(b'4')
                print("Obstaculo cercano -> enviar (4)")
                modo_bloqueado = True
        elif 10 <= distancia <= 20:
            if not modo_bloqueado:
                ser.write(b'2')
                print("Distancia media -> enviar (2)")
        else:
            modo_bloqueado = False
        time.sleep(0.1)

# (El resto del codigo original permanece igual)

# Agrega al final de main:

def main():
    url = "http://192.168.1.2:4747/video"
    captura = cv2.VideoCapture(url)
    if not captura.isOpened():
        print("Error al conectar con la camara")
        return

    hilo_ultra = threading.Thread(target=control_ultrasonico, daemon=True)
    hilo_ultra.start()

    hilo_video = threading.Thread(target=procesar_video, args=(captura,), daemon=True)
    hilo_video.start()

    iniciar_gui()
    hilo_video.join()
    GPIO.cleanup()

if __name__ == "__main__":
    main()
