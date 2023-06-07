import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
from functions import calculate_the_angles
import matplotlib.pyplot as plt
import time
from collections import deque
from statistics import mean



import cv2
import numpy as np
import socket
import struct

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
from models import model_indice
from models import model_medio
from models import model_anular
from models import model_menique
from models import model_pulgar


# Crear una cola con tamaño fijo
pred_0 = deque(maxlen=30)
pred_1 = deque(maxlen=30)
pred_2 = deque(maxlen=30)
pred_3 = deque(maxlen=30)
pred_4 = deque(maxlen=30)

axis_time = deque(maxlen=30)

# Configurar el gráfico inicial
plt.ion()  # Habilitar el modo interactivo
fig, ax = plt.subplots()
linea_0, = ax.plot([], pred_0)  # Línea inicial vacía
linea_1, = ax.plot([], pred_1)  # Línea inicial vacía
linea_2, = ax.plot([], pred_2)  # Línea inicial vacía
linea_3, = ax.plot([], pred_3)  # Línea inicial vacía
linea_4, = ax.plot([], pred_4)  # Línea inicial vacía

# Configurar el rango de los ejes x e y
ax.set_ylim(-0.25, 1.5)  # Rango del eje y

# Variable para el tiempo inicial
tiempo_inicial = time.time()
tiempo_actualizacion = tiempo_inicial



# Configuración del servidor
SERVER_IP = '192.168.1.78'  # Dirección IP del servidor
SERVER_PORT = 5000  # Puerto de escucha

# Inicializar el socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))

UDP_MAX_SIZE = 65507


try:
	with mp_hands.Hands(
    model_complexity=1,
    min_detection_confidence=0.5,
		min_tracking_confidence=0.8) as hands:

		while True:
				frame_data, client_address = server_socket.recvfrom(UDP_MAX_SIZE)

				# Convertir el frame recibido a una imagen
				frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)

				if frame is None:
					continue

				image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				results = hands.process(image)

				# Draw the hand annotations on the image.
				# image.flags.writeable = True
				# image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
				if results.multi_hand_landmarks:
				# 	mp_drawing.draw_landmarks(
				# 		image,
				# 		results.multi_hand_landmarks[0],
				# 		mp_hands.HAND_CONNECTIONS,
				# 		mp_drawing_styles.get_default_hand_landmarks_style(),
				# 		mp_drawing_styles.get_default_hand_connections_style())

					angles = calculate_the_angles(results.multi_hand_landmarks[0])
					#motion predictions of servomotors
					tiempo_actual = time.time()
					axis_time.append(tiempo_actual - tiempo_inicial)

					pred_0.append(model_indice.predict((angles[0],)))
					pred_1.append(model_medio.predict((angles[1],)))

					pred_2.append(model_anular.predict((angles[2],)))
					pred_3.append(model_menique.predict((angles[3],)))
					pred_4.append(model_pulgar.predict((angles[4],)))
					pred_4[-1] = (pred_4[-1]-0.4) / 2

					plt.pause(0.1)
					
					linea_0.set_data(axis_time, pred_0)
					linea_1.set_data(axis_time, pred_1)
					linea_2.set_data(axis_time, pred_2)
					linea_3.set_data(axis_time, pred_3)

					linea_4.set_data(axis_time, pred_4)
					ax.relim()
					ax.autoscale_view()
					# Redibujar el gráfico
					fig.canvas.draw()
					# Agregar una pausa para controlar la velocidad de actualización
					

				# Flip the image horizontally for a selfie-view display.
				cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
				if cv2.waitKey(5) & 0xFF == 27:
					break

finally:
	server_socket.close()







