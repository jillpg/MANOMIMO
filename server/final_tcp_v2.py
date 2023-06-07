
"""notas, error en la sincronizacion de recepcion y envios de datos, asi que primero probar a solo recibir datos"""

import cv2
import numpy as np
import socket
import struct
import pickle

from functions import calculate_the_angles
import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import time
from collections import deque
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

import joblib

model_pulgar     = joblib.load('model_pulgar.pkl')
model_indice     = joblib.load('model_indice.pkl')
model_medio      = joblib.load('model_medio.pkl')
model_anular     = joblib.load('model_anular.pkl')
model_menique    = joblib.load('model_menique.pkl')



# Crear una cola con tamaño fijo

#guardo los valores predecidos inicial r0 y final r1 para mover el servo en 1s (30fps)
pred_0 = deque(maxlen=30)
pred_1 = deque(maxlen=30)
pred_2 = deque(maxlen=30)
pred_3 = deque(maxlen=30)
pred_4 = deque(maxlen=30)

#axis_time = deque(maxlen=30)

# Variable para el tiempo inicial
tiempo_inicial = time.time()
tiempo_actualizacion = tiempo_inicial

# Configuración del servidor
SERVER_IP = '192.168.1.78'  # Dirección IP del servidor
SERVER_PORT = 5000  # Puerto de escucha

# Inicializar el servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(1)
print('Esperando conexión...')

# Aceptar la conexión del cliente
client_socket, client_address = server_socket.accept()
print('Cliente conectado:', client_address)

# Crear una interfaz para recibir los datos
connection = client_socket.makefile('rb')

frames = deque(maxlen=30) #max 30 frames = 1segundo

# funcion de suavizacion:
# ventajas: movimiento mas natural
# desventajas: procesar todos los frames conlleva un tiempo mayor de proceso

# latencia de 1s -> 30frames
# si se mueve en tiempo real acumulando frames de 1s, procesa 30 frames, luego para mover los siguientes
# 1s hay un intervalo de 300 milisegundos que es lo que procesa los frames.
# desventajas: no es en tiempo real sino que son interaciones de 1s de tiempo real desconectada por X ms de otras iteraciones.
# ventajas: puedo procesar trozos de videos grabados con un timing perfecto porque puedo aplicar funcion de suavizacion

#latencia de 0.03s -> 1frame
# si es una latencia de 0.03 procesa 1 frame, hay un intervalo de 10 milisegundo de proceso, puedo concatenar las iteraciones
# para compensar el tiempo de procesado para que parezca tiempo real (p e: ejecutar el movimiento en 0.03+0.01=0.04s y no en 0.03)
# asi mientras esta en 0.03 hasta 0.04, un hilo ya tendra procesado el siguiente frame.
# desventajas: dificil de calibrar porque el tiempo entre interaciones no es solo del proceso sino tambien de la red
# desventajas: cambiar de ubicacion, distancia entre cliente y servidor, etc alteraria los valores
# desventajas: no habria funcion de suavizacion
# solucion: crear un programa inteligente que varie los parametros para ajustar segun las condiciones, pero seria dificil.
# ventajas: si se consigue, seria un programa tiempo real.

#latencia < 0.03 (si el tiempo de conexion y proceso)
# otra alternativa es usar hilos para el proceso y prediccion de los frames capturados, ademas de un hilo para la recepcion y envio de frames.
# si añadimos el programa inteligente que compensa el tiempo de proceso y transferencia de datos
# esta seria la solucion ideal
latency = 1



try:

    with mp_hands.Hands(
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.8) as hands:
        while True:
            # Recibir el tamaño del frame
            frame_size_data = connection.read(struct.calcsize('<L'))

            if frame_size_data is None:
                logging.debug(f'frame recibido de tamaño: {frame_size_data}')
                continue
            frame_size = struct.unpack('<L', frame_size_data)[0]

            # Recibir el frame
            frame_data = connection.read(frame_size)
            # Convertir el frame recibido a una imagen
            frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)

            if frame is None:
                logging.debug('frame recibido es None')
                continue


            logging.debug('frame recibido correctamente')
            frames.append(frame)

            tiempo_actual = time.time()


            if (tiempo_actual - tiempo_inicial) < latency:
                logging.debug(f'aun no pasaron {int(latency)}s, recolectando frames ...')
                continue

            logging.debug(f'ha pasado {int(latency)}s, procesamos los frames')
            tiempo_inicial = tiempo_actual

            to_send = []

            for i, f in enumerate(frames):
                cv2.imshow('Frame', frame)
                cv2.waitKey(1)

            for i, f in enumerate(frames):
                results = hands.process(frame)
                if results.multi_hand_landmarks:
                    logging.debug(f'procesamos frame: {i}')
                    # calculamos los angulos de un frame
                    angles = calculate_the_angles(results.multi_hand_landmarks[0])
                    #prediccion de cada dedo
                    to_send.append(model_indice.predict((angles[0],)))
                    to_send.append(model_medio.predict((angles[1],)))
                    to_send.append(model_anular.predict((angles[2],)))
                    to_send.append(model_menique.predict((angles[3],)))
                    to_send.append(model_pulgar.predict((angles[4],)))
                    # tengo una lista de 1 frame: [0.4, 0.6, 0.7, 0.2, 0.4]

            #suavizar results
           
            #convertimos a una lista de valores
            to_send_list = [float(arr[0]) for arr in to_send]
            print(f'valores a enviar: {to_send_list}')

             # Serializar la lista como bytes
            values_bytes = pickle.dumps(to_send_list)
            logging.debug('enviamos los valores predecidos')
            # Enviar los bytes al cliente
            client_socket.sendall(values_bytes)

finally:
    connection.close()
    client_socket.close()
    server_socket.close()
