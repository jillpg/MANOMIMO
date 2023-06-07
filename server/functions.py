import mediapipe as mp
import cv2 as cv
import os
import math
import pandas as pd
import numpy as np

# Temporalmente son solo de 4 dedos (añadir pulgar mas adelante)

# calcula 3 angulos de las articulaciones de cada dedo, en orden descendente
# (desde las articulaciones superiores hasta las inferiores). Esto de los de 4 dedos de la mano (excluyendo el pulgar)

def calculate_the_angles(results):
    hand_angles = {}
    despl = 0

    for i in range(5):
        #angulos superiores

        vector1 = [results.landmark[4+despl].x - results.landmark[3+despl].x, results.landmark[4+despl].y - results.landmark[3+despl].y, results.landmark[4+despl].z - results.landmark[3+despl].z]
        vector2 = [ results.landmark[2+despl].x-results.landmark[3+despl].x, results.landmark[2+despl].y - results.landmark[3+despl].y,  - results.landmark[2+despl].z - results.landmark[2+despl].z]

        # Calcula el producto cruz entre los vectores
        producto_cruz = [vector1[1] * vector2[2] - vector1[2] * vector2[1],
                            vector1[2] * vector2[0] - vector1[0] * vector2[2],
                            vector1[0] * vector2[1] - vector1[1] * vector2[0]]
        # Calcula el ángulo en radianes usando el producto cruz
        angulo_radianes = math.atan2(math.sqrt(sum(i**2 for i in producto_cruz)), sum(vector1[i] * vector2[i] for i in range(len(vector1))))
        # Convierte el ángulo de radianes a grados
        angulo_grados = math.degrees(angulo_radianes)
        hand_angles[i] = [angulo_grados]


        #angulos del medio
        vector1 = [results.landmark[3+despl].x - results.landmark[2+despl].x, results.landmark[3+despl].y - results.landmark[2+despl].y, results.landmark[3+despl].z - results.landmark[2+despl].z]
        vector2 = [results.landmark[1+despl].x - results.landmark[2+despl].x, results.landmark[1+despl].y - results.landmark[2+despl].y, results.landmark[1+despl].z - results.landmark[2+despl].z]
        # Calcula el producto cruz entre los vectores
        producto_cruz = [vector1[1] * vector2[2] - vector1[2] * vector2[1],
                            vector1[2] * vector2[0] - vector1[0] * vector2[2],
                            vector1[0] * vector2[1] - vector1[1] * vector2[0]]
        # Calcula el ángulo en radianes usando el producto cruz
        angulo_radianes = math.atan2(math.sqrt(sum(i**2 for i in producto_cruz)), sum(vector1[i] * vector2[i] for i in range(len(vector1))))
        # Convierte el ángulo de radianes a grados
        angulo_grados = math.degrees(angulo_radianes)
        hand_angles[i].append(angulo_grados)


        #angulos inferior (respecto al punto inferior: 0 de la palma)
        vector1 = [results.landmark[2+despl].x - results.landmark[1+despl].x, results.landmark[2+despl].y - results.landmark[1+despl].y, results.landmark[2+despl].z - results.landmark[1+despl].z]
        vector2 = [results.landmark[0].x - results.landmark[1+despl].x, results.landmark[0].y - results.landmark[1+despl].y, results.landmark[0].z - results.landmark[1+despl].z]
        # Calcula el producto cruz entre los vectores
        producto_cruz = [vector1[1] * vector2[2] - vector1[2] * vector2[1],
                            vector1[2] * vector2[0] - vector1[0] * vector2[2],
                            vector1[0] * vector2[1] - vector1[1] * vector2[0]]
        # Calcula el ángulo en radianes usando el producto cruz
        angulo_radianes = math.atan2(math.sqrt(sum(i**2 for i in producto_cruz)), sum(vector1[i] * vector2[i] for i in range(len(vector1))))
        # Convierte el ángulo de radianes a grados
        angulo_grados = math.degrees(angulo_radianes)
        hand_angles[i].append(angulo_grados)
        despl+=4
    return hand_angles



def video_to_images(video_path, output_folder, class_name, index_video):

    video = cv.VideoCapture(video_path)
    if not video.isOpened():
        print("Error al abrir el video.")
        return
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    frame_count = 0
    img_saved_count = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break
        #se guarda un frame cada 10 frames
        if frame_count % 10 == 0:
            image_path = os.path.join(output_folder, f"{class_name}_{index_video}_{img_saved_count:04d}.jpg")
            cv.imwrite(image_path, frame)
            img_saved_count+=1
        frame_count += 1
    video.release()



#considerating the class name is inside the file name, return list containing all the angles of each image with its class (temporarily 4 fingers)
def dataset_angles(data_dir: str, my_classes:dict):

    files = os.listdir(data_dir)
    mp_hands = mp.solutions.hands
    img_angles_with_class = []
    with mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5) as hands:
        for class_name in my_classes:
            IMAGE_FILES = [file for file in files if file.startswith(class_name)]
            for idx, file in enumerate(IMAGE_FILES):
				# Read an image, flip it around y-axis for correct handedness output (see
				# above).
                image = cv.imread(data_dir+file)
				# Convert the BGR image to RGB before processing.
                results = hands.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))
                if not results.multi_hand_landmarks:
                    print(f'NO RESULTS: {idx}')
                    continue

                angles = calculate_the_angles(results.multi_hand_landmarks[0])
                img_angles_with_class.append((angles, my_classes[class_name]))
    return img_angles_with_class











