import cv2
import serial
import time

# ----------- CONFIGURACIoN -----------
DROIDCAM_URL = "http://192.168.1.2:4747/video"
UART_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200

# ----------- INICIALIZACIoN -----------
ser = serial.Serial(UART_PORT, BAUD_RATE, timeout=1)
time.sleep(2)

cap = cv2.VideoCapture(DROIDCAM_URL)
if not cap.isOpened():
    print("No se pudo abrir el stream de DroidCam.")
    exit(1)

print("Iniciando rastreo de objeto rojo...")

# ----------- BUCLE PRINCIPAL -----------
while True:
    ret, frame = cap.read()
    if not ret:
        print("No se recibio frame.")
        break
	#obtengo el hsv de cada frame
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Rango para color rojo (ajustable)
    #las mascaras son "una hoja de color" la cual me permite trabajar con ciertas tonaliades
    #mask1 y mask2 son usados para marcar umbrales de hsv(hue,saturation,value) los valores del primer parentesis es el umbral bajo y el 2do el alto 
    mask1 = cv2.inRange(hsv, (0, 100, 100), (10, 255, 255))      # Rojo bajo
    mask2 = cv2.inRange(hsv, (160, 100, 100), (180, 255, 255))   # Rojo alto
    #suma las 2 mascaras para tener un buen umbral, se usa or para ser un poco mas flexibles con las tonalidades
    mask = cv2.bitwise_or(mask1, mask2)

    # Encontrar contornos
    #Usando la mask(mascara) como primer arguemnto voy a usar retr_external para extraer contornos y usa chain_approx_simple para quitar redundancias, si se quieren mantener se usara contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #red_objecst, detecta los contornos dentro de un determinado area y con esto se filtran colores rojos peuqenos
    red_objects = [cnt for cnt in contours if cv2.contourArea(cnt) > 500]  # filtrar ruido
	#con len se calcula el numero de iteraciones en el objeto, en pocas cuantos contornos detecto
    num_objects = len(red_objects)

    if num_objects == 1:
        # Seguir un solo objeto
        ser.write(b'1')
        cv2.drawContours(frame, red_objects, -1, (0, 255, 0), 2)
        print("1 objeto rojo detectado ? seguir (1)")
    elif num_objects >= 2:
        # Alerta por multiples objetos
        ser.write(b'2')
        cv2.drawContours(frame, red_objects, -1, (0, 0, 255), 2)
        print(f"{num_objects} objetos rojos detectados ? alerta (2)")
    else:
        # No se detecta nada ? girar
        ser.write(b'3')
        print("Ningun objeto rojo detectado ? buscar (3)")

    # Mostrar video
    cv2.imshow("DroidCam Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ----------- FINALIZACIoN -----------
cap.release()
cv2.destroyAllWindows()
ser.close()
