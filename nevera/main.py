#By Juan David Cuscagua López

from itertools import count
from lib2to3.pgen2.token import GREATER
from string import octdigits
import cv2
import numpy as np
import urllib.request
import joblib

def nothing(x):
    pass

def showImgW(nameWindow, matImage):
    cv2.imshow(nameWindow, matImage)

def showImg(nameWindow, matImage, t):
    cv2.imshow(nameWindow, matImage)
    cv2.waitKey(t)

capture = cv2.VideoCapture("videos/13.mp4")

model_ss = joblib.load('model_ss.pkl')
model_svm = joblib.load('model_svm.pkl')

frame_counter = 0
aguacaticos_cantidad = 0
compotas_cantidad = 0
juguitos_cantidad = 0
limoncitos_cantidad = 0
malticas_cantidad = 0
manzanitas_cantidad = 0
espacios_disponibles = 0

while(capture.isOpened()):
    ret, inv_frame = capture.read()
    if ret==False:
            break

    frame_counter += 1
    frame = cv2.flip(inv_frame,-1)
    width = int(frame.shape[1] * 0.3)
    height = int(frame.shape[0] * 0.3)
    dim = (width, height)
    imgColor = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    
    if cv2.waitKey(1) & 0xFF == ord ('a'):
        img_train = []
        aguacaticos_cantidad = 0
        compotas_cantidad = 0
        juguitos_cantidad = 0
        limoncitos_cantidad = 0
        malticas_cantidad = 0
        manzanitas_cantidad = 0
        espacios_disponibles = 0
        roi_limones = imgColor[366:416, 126:341]
        width = int(roi_limones.shape[1] * 0.25)
        height = int(roi_limones.shape[0])
        for i in range(4):
            img_train.append(roi_limones[0:height, i*width:(i+1)*width])
        # Juguitos
        roi_juguitos = imgColor[459:579, 126:319]
        width = int(roi_juguitos.shape[1] * 1/3)
        height = int(roi_juguitos.shape[0]*0.5)
        for i in range(2):
            for j in range(3):
                img_train.append(roi_juguitos[i*height:(i+1)*height, j*width:(j+1)*width])
        # Manzananitas
        roi_manzanitas = imgColor[695:760, 103:332]
        width = int(roi_manzanitas.shape[1] * 1/3)
        height = int(roi_manzanitas.shape[0]*1)
        for i in range(3):
            img_train.append(roi_manzanitas[0:height, i*width:(i+1)*width])
        # Repisa_1
        roi_repisa_1 = imgColor[382:471, 371:557]
        width = int(roi_repisa_1.shape[1] * 0.5)
        height = int(roi_repisa_1.shape[0]*1)
        for i in range(2):
            img_train.append(roi_repisa_1[0:height, i*width:(i+1)*width])
        # Repisa_2
        roi_repisa_2 = imgColor[513:610, 368:547]
        width = int(roi_repisa_2.shape[1] * 0.5)
        height = int(roi_repisa_2.shape[0]*1)
        for i in range(2):
            img_train.append(roi_repisa_2[0:height, i*width:(i+1)*width])
        # Repisa_3
        roi_repisa_3 = imgColor[665:765, 374:553]
        width = int(roi_repisa_3.shape[1] * 0.5)
        height = int(roi_repisa_3.shape[0]*1)
        for i in range(2):
            img_train.append(roi_repisa_3[0:height, i*width:(i+1)*width])
        
        for i in img_train:
            vector_pixel = []
            for a in cv2.resize(i,(25,50)):
                for b in a:
                    for c in b:
                        vector_pixel.append(c)
            vectorCarac=np.array(vector_pixel,dtype=np.float32)
            vc_r = vectorCarac.reshape(1, -1)
            vc_ss = model_ss.transform(vc_r)
            result_predict = model_svm.predict(vc_ss)
            if result_predict == 0:
                aguacaticos_cantidad += 1
            elif result_predict == 1:
                compotas_cantidad += 1
            elif result_predict == 2:
                juguitos_cantidad += 1
            elif result_predict == 3:
                limoncitos_cantidad += 1
            elif result_predict == 4:
                malticas_cantidad += 1
            elif result_predict == 5:
                manzanitas_cantidad += 1
            else:
                espacios_disponibles += 1


        
    cv2.putText(imgColor,'Aguacaticos: ' + str(aguacaticos_cantidad), (100,25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
    cv2.putText(imgColor,'Compotas: ' + str(compotas_cantidad), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
    cv2.putText(imgColor,'Juguitos: ' + str(juguitos_cantidad), (100,75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
    cv2.putText(imgColor,'Limoncitos: ' + str(limoncitos_cantidad), (100,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
    cv2.putText(imgColor,'Malticas: ' + str(malticas_cantidad), (300,25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
    cv2.putText(imgColor,'Manzanitas: ' + str(manzanitas_cantidad), (300,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
    cv2.putText(imgColor,'Espacios disponibles: ' + str(espacios_disponibles), (300,75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)

    showImgW("imgColor", imgColor[0:800, :])