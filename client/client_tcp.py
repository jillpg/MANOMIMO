import cv2
import numpy as np
import socket
import struct
import pickle
import time
from adafruit_pca9685 import PCA9685
import board
import busio
import adafruit_motor.servo
import logging

# Configurar el logger
logging.basicConfig(level=logging.DEBUG , format='%(asctime)s - %(levelname)s - %(message)s')


# # Initialize the PCA9685 controller
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c,address=0x40)
servo=[]

pca.frequency = 25  # Set the PWM frequency (adjust if necessary)
for i in range(5):     
    servo_channel=pca.channels[i]     
    servo.append(adafruit_motor.servo.Servo(servo_channel))   

# Configuración del servidor
SERVER_IP = '192.168.1.78'  # Reemplaza con la dirección IP de tu portátil servidor
SERVER_PORT = 5000  # Puerto de escucha en el servidor

# Configuración de la cámara
CAMERA_INDEX = 0  # Índice de la cámara (puede ser 0, 1, etc., dependiendo de la configuración)

# Establecer la conexión con el servidor
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))
connection = client_socket.makefile('wb')

# Configuración del tiempo de espera en segundos
TIMEOUT = 0.05

# Establecer el tiempo de espera en el socket
client_socket.settimeout(TIMEOUT)


# Inicializar la cámara
logging.debug('iniciando camara')
camera = cv2.VideoCapture(CAMERA_INDEX)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Ancho del frame
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Alto del frame

try:
    while True:
        # Capturar frame de la cámara
        logging.debug('capturando frames camara')
        ret, frame = camera.read()

    
        # Codificar el frame como una cadena de bytes
        frame_data = cv2.imencode('.jpg', frame)[1].tobytes()

        # Enviar el tamaño del frame al servidor
        frame_size = struct.pack('<L', len(frame_data))
        client_socket.sendall(frame_size)

        # Enviar el frame al servidor
        logging.debug('enviamos un frame')
        client_socket.sendall(frame_data)


        try:
            # Recibir los bytes de la lista desde el servidor
            values_bytes = client_socket.recv(4096)

        except socket.timeout:
            logging.debug('No se recibieron datos del servidor dentro del tiempo de espera')
            continue
        
        logging.debug('ha recibido valores del servidor')
        # Deserializar los bytes en una lista de valores float
        values = pickle.loads(values_bytes) 

        print(values)


        for i, value in enumerate(values):
            values[i] = value*180
            if value>180:
                values[i] = 180
            if value<0:
                values[i] = 0


        values_sz = len(vales)
        num_frames = len(vales/5)


       for i in range(num_frames):
            v_1 = values[5*(i):5*(i+1)]
            for i in range(5):
                servo[4].angle=v_1[0]
                servo[3].angle=v_1[1]
                servo[2].angle=v_1[2]
                servo[1].angle=v_1[3]
                servo[0].angle=v_1[4]     
                time.sleep(0.03)


finally:
    camera.release()
    connection.close()
    client_socket.close()
