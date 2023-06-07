
import cv2
import numpy as np
import socket
import struct
import pickle

from functions import calculate_the_angles
import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
from func_suavizado import *
import matplotlib.pyplot as plt
import time
from collections import deque
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
from models import model_indice
from models import model_medio
from models import model_anular
from models import model_menique
from models import model_pulgar



# Crear una cola con tamaño fijo
r0_pred_0 = deque(maxlen=30)
r0_pred_1 = deque(maxlen=30)
r0_pred_2 = deque(maxlen=30)
r0_pred_3 = deque(maxlen=30)
r0_pred_4 = deque(maxlen=30)

r1_pred_0 = deque(maxlen=30)
r1_pred_1 = deque(maxlen=30)
r1_pred_2 = deque(maxlen=30)
r1_pred_3 = deque(maxlen=30)
r1_pred_4 = deque(maxlen=30)

axis_time = deque(maxlen=30)


# # Configurar el gráfico inicial
# plt.ion()  # Habilitar el modo interactivo
# fig, ax = plt.subplots()
# linea_0, = ax.plot([], pred_0)  # Línea inicial vacía
# linea_1, = ax.plot([], pred_1)  # Línea inicial vacía
# linea_2, = ax.plot([], pred_2)  # Línea inicial vacía
# linea_3, = ax.plot([], pred_3)  # Línea inicial vacía
# linea_4, = ax.plot([], pred_4)  # Línea inicial vacía


# # Configurar el rango de los ejes x e y
# ax.set_ylim(-0.25, 1.5)  # Rango del eje y

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
time_to_process = 0
try:

    with mp_hands.Hands(
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.8) as hands:
        while True:
            # Recibir el tamaño del frame
            frame_size_data = connection.read(struct.calcsize('<L'))
            frame_size = struct.unpack('<L', frame_size_data)[0]

            # Recibir el frame
            frame_data = connection.read(frame_size)
            # Convertir el frame recibido a una imagen
            frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)

            if frame is None:
                logging.debug('frame recibido es None')
                continue
            
            logging.debug('frame recivido correctamente')
            tiempo_actual = time.time()

            # Mostrar el frame procesado
            # cv2.imshow('Frame', frame)
            # cv2.waitKey(1)

            if tiempo_actual - tiempo_inicial < 0.1:
                logging.debug('aun no pasaron 0.1s')
                continue


            #ha pasado 0.1s cogemos un frame
            logging.debug('ha pasado 0.1s, añadimos un frame')
            tiempo_inicial = tiempo_actual

            frames.append(frame)

            if len(frames) < 2:
                logging.debug('aun no tenemos 2 frames')
                continue

            #hay 2 o mas 2 frames
            logging.debug('tenemos 2 frames')
            frame_1 = frames.pop()
            frame_0 = frames.pop()


            #frame_0 = cv2.cvtColor(frame_0, cv2.COLOR_BGR2RGB)
            #frame_1 = cv2.cvtColor(frame_1, cv2.COLOR_BGR2RGB)

            logging.debug('procesamos frame0')
            results_0 = hands.process(frame_0)
            if results_0.multi_hand_landmarks[0]:
                angles_0 = calculate_the_angles(results_0.multi_hand_landmarks[0])

            logging.debug('procesamos frame1')
            results_1 = hands.process(frame_1)
            if results_1.multi_hand_landmarks[0]:
                angles_1 = calculate_the_angles(results_1.multi_hand_landmarks[0])


            to_send = []
            to_send.append(model_indice.predict((angles_0[0],)))
            to_send.append(model_medio.predict((angles_0[1],)))
            to_send.append(model_anular.predict((angles_0[2],)))
            to_send.append(model_menique.predict((angles_0[3],)))
            to_send.append(model_pulgar.predict((angles_0[4],)))
            to_send.append(model_indice.predict((angles_1[0],)))
            to_send.append(model_medio.predict((angles_1[1],)))
            to_send.append(model_anular.predict((angles_1[2],)))
            to_send.append(model_menique.predict((angles_1[3],)))
            to_send.append(model_pulgar.predict((angles_1[4],)))

            # Serializar la lista como bytes
            values_bytes = pickle.dumps(to_send)

            logging.debug('enviamos los valores predecidos')
            # Enviar los bytes al cliente
            client_socket.sendall(values_bytes)





            # Realizar el procesamiento del frame (aquí puedes añadir tu lógica personalizada)




finally:
    connection.close()
    client_socket.close()
    server_socket.close()
