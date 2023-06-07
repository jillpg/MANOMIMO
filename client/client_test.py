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
import select

# Configurar el logger
logging.basicConfig(level=logging.DEBUG , format='%(asctime)s - %(levelname)s - %(message)s')



# Configuración del servidor
SERVER_IP = '192.168.1.78'  # Reemplaza con la dirección IP de tu portátil servidor
SERVER_PORT = 5000  # Puerto de escucha en el servidor

# Configuración de la cámara
CAMERA_INDEX = 0  # Índice de la cámara (puede ser 0, 1, etc., dependiendo de la configuración)

# Establecer la conexión con el servidor
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))
connection = client_socket.makefile('wb')

# Configuración del tiempo de espera en segundos, calcular el tiempo maximo que tardara en procesar el servidor
TIMEOUT = 1

# Establecer el tiempo de espera en el socket
client_socket.settimeout(TIMEOUT)


# Inicializar la cámara
logging.debug('iniciando camara')
camera = cv2.VideoCapture(CAMERA_INDEX)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Ancho del frame
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Alto del frame

tiempo_inicio = time.time()
tiempo_actual = time.time()

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
        


        #si terminamos de enviar los frames de 1segundo, esperamos a recibir valores
        #el timeout es el tiempo maximo de proceso de  los frames del servidor

        ready_to_read, _, _ = select.select([client_socket], [], [], 0)
        if ready_to_read:
            try:
                # Recibir los bytes de la lista desde el servidor
                values_bytes = client_socket.recv(4096)
                values = pickle.loads(values_bytes)
                print(values)

            except socket.timeout:
                print('No se recibieron datos del servidor dentro del tiempo de espera')
                continue



        # if (tiempo_actual - tiempo_inicio) >= 1:
        #     try:
        #         # Recibir los bytes de la lista desde el servidor
        #         values_bytes = client_socket.recv(4096)
        #         values = pickle.loads(values_bytes) 
        #         print(values)

        #     except socket.timeout:
        #         print('No se recibieron datos del servidor dentro del tiempo de espera')
        #         continue
        

finally:
    camera.release()
    connection.close()
    client_socket.close()
