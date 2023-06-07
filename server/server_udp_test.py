import cv2
import numpy as np
import socket
import struct

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

try:
    while True:
        # Recibir el tamaño del frame
        frame_size_data = connection.read(struct.calcsize('<L'))
        frame_size = struct.unpack('<L', frame_size_data)[0]

        # Recibir el frame
        frame_data = connection.read(frame_size)

        # Convertir el frame recibido a una imagen
        frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)

        # Realizar el procesamiento del frame (aquí puedes añadir tu lógica personalizada)
        # Por ejemplo, podrías aplicar detección de objetos, reconocimiento facial, etc.


        # Mostrar el frame procesado
        cv2.imshow('Frame', frame)
        cv2.waitKey(1)

finally:
    connection.close()
    client_socket.close()
    server_socket.close()
