# RLP-ManoMimo
Robòtica, Llenguatge i Planificació, Curs 2022-23 Project

Presentation
https://docs.google.com/presentation/d/1vV7Lt88RAJG0M1EuOl8PxVXpeFjewRLk/edit?usp=drivesdk&ouid=113962539030239291082&rtpof=true&sd=true

Video
https://drive.google.com/file/d/1RJNWA-_TOiXyENVviEDPJt_26m2_ebH8/view?usp=drivesdk


<img src="https://raw.githubusercontent.com/1568079/img/main/main.png" align="right" width="410" alt="header pic"/>

# Table of Contents
   * [What is this?](#what-is-this)
   * [Requirements](#requirements)
   * [Documentation](#documentation)
   * [Client-Server connection](#client-server-connection)
      * [Client](#client)
      * [Server](#server)
   * [Hand Detection](#hand-detection)
      * [Mediapipe landmark detection](#mediapipe-landmark-detection)
      * [Angles function](#angles-function)
      * [Finger models](#finger-models)
   * [Use-case](#use-case)
   * [Contribution](#contribution)
   * [Citing](#citing)
   * [Support](#support)
   * [Sponsors](#sponsors)
   * [Authors](#authors)

# What is this?

This is a collection of codes to make a robotic hand mimic movements

Features:

1. Easy to read, well-structured and well commented.

2. There are tests of different types of servers and the most optimal ones are selected.

3. The code ranges from models to train fingers, landmark detection and servers to transfer information.


# Requirements

For running:

- [Python 3.11.x](https://www.python.org/)
- [OpenCV 4.4.0](https://opencv.org/)
- [Raspbian buster](https://downloads.raspberrypi.org/raspbian/images/raspbian-2019-07-12/)
- [Mediapipe](https://pypi.org/project/mediapipe/)

For development:
  
- [Matplotlib](https://matplotlib.org/stable/users/installing/index.html) (to view the results)


# Documentation

This README only shows our progress in the project and the different tests that we have been carrying out.

If you want to improve it, you can try more advanced models and different types of clients and servers.

# Client-Server connection

Regarding the client-server connection, we have tested 2 types:
- TCP
- UDP

Finally, we have stayed with the TCP because when we receive frames from the camera we do not want to run the risk of them being lost because then the movements would be different from the real ones.

When doing the tests between the two, we thought that UDP would be faster than TCP, but it was something that we denied in a short time, since the times were almost identical. That made the decision even easier.

## Client

The most important thing to know is:

1. You can vary the frequency of the servos if necessary using the pca.frequency in line 22.

2. The server IP is added by SERVER_IP in line 28.

3. The server listening port is selected by SERVER_PORT on line 29

4. You can modify the camera index by CAMERA_INDEX in line 32

5. You can adjust the timeout using TIMEOUT on line 40, depending on the type of connection you have. The slower, the more timeout will be necessary.

6. You can modify the size of the image by varying camera.set(cv2.CAP_PROP_FRAME_WIDTH, X) for the width and camera.set(cv2.CAP_PROP_FRAME_HEIGHT, Y) for the height on lines 49 and 50

## Server

The most important thing to know is:

1. As in the client, the server IP and the listening port are selected using SERVER_IP and SERVER_PORT in lines 51 and 52

2. Latency can be modified, which is the time that the hand records, then it is processed and sent to the client. It is explained in depth in the code on line 93

# Hand detection

We have used Mediapipe landmark detection to recognize the coordinates of the landmarks, using the function calculate_the_angles from the coordinates we obtain the angles of the joints of the fingers, and this is the dataset that the models train to predict if the hand is extended or closed.

## Mediapipe landmark detection

The MediaPipe Hand Landmarker task lets you detect the landmarks of the hands in an image.

See further below for an image of this functionality that MediaPipe provides for hand recognition, this package is able to identify, locate and provide a unique number for each joint on both your hands. 

<img src="https://developers.google.com/static/mediapipe/images/solutions/hand-landmarks.png" width="640" alt="MEDIAPIPE pic">


## Angles function

We calculate the three angles of the joints of each finger, in descending order, following the following steps:
1. We calculate the cross product between the vectors

2. We calculate the angle in radians using the cross product

3. We convert the angle from radians to degrees

## Finger models

Dataframe de los angulos de las articulaciones de un dedo: <br> <br>
<img src="https://raw.githubusercontent.com/1568079/img/main/Dataframe%20de%20los%20angulos%20de%20las%20articulaciones%20de%20un%20dedo.png" width="320" alt="DATAFRAME pic">

GRAFICO DE DISPERSION <br>
Generamos una nube de puntos para ver la correlacion entre una de las articulaciones y la clase (si las falanges estan extendidas o flexionadas): <br> <br>
<img src="https://raw.githubusercontent.com/1568079/img/main/GRAFICO%20DE%20DISPERSION.png" width="640" alt="DISPERSIÓN pic">

Regresion lineal y evaluacion (MSE Y R^2): <br> <br>
<img src="https://raw.githubusercontent.com/1568079/img/main/Regresion%20lineal%20y%20evaluacion%20(MSE%20Y%20R%5E2).png" alt="ANÁLISIS pic">

# Use-case

If this project helps your robotics project, please let us know with creating an Issue with the title Use-case.

Your robot's video is very welcome!!

# Contribution

Contributions are always welcome! Please submit a Pull Request.

# Citing

If you use this project's code for your academic work, we encourage you to cite it.

If you use this project's code in industry, we'd love to hear from you as well; feel free to reach out to the developers directly.

# Support

If you have any issues, please create an Issue.

# Sponsors

This project is proudly supported by:

### Universidad Autónoma de Barcelona (UAB)

We're immensely grateful for the support provided by the **Universidad Autónoma de Barcelona**, our home institution. The academic knowledge, facilities, and inspiring environment at UAB have been crucial to the success of this project.

We invite other potential sponsors interested in supporting our project to contact us.

# Authors

- Joel Marco Quiroga Poma 1504249

- Arnau Tena González 1526414

- Jill Areny Palma Garro 1604284

- Martí Rius Ollé 1568079
