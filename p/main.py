#By Juan David Cuscagua López

from itertools import count
from lib2to3.pgen2.token import GREATER
from string import octdigits
import cv2
import numpy as np
import urllib.request

def nothing(x):
    pass
def showImgW(nameWindow, matImage):
    cv2.imshow(nameWindow, matImage)
def showImg(nameWindow, matImage, t):
    cv2.imshow(nameWindow, matImage)
    cv2.waitKey(t)

capture = cv2.VideoCapture("video.mp4")

cv2.namedWindow('windTrack1')
cv2.createTrackbar('u1', 'windTrack1', 0, 255, nothing)        # u1 = umbral

cv2.namedWindow('windTrack2')
cv2.createTrackbar('u2', 'windTrack2', 0, 255, nothing)        # u2 = umbral

grandes = 0
medianos = 0
pequeños = 0
grandes_salen = 0
medianos_salen = 0
pequeños_salen = 0
frame_counter = 0
last_frame_counter = 0
last_frame_counter_salen = 0
while(capture.isOpened()):
    ret, frame = capture.read()
    frame_counter += 1
    if (cv2.waitKey(30) & 0xFF == ord ('q')) or ret==False:
            break
    u1 = cv2.getTrackbarPos('u1', 'windTrack1')
    u2 = cv2.getTrackbarPos('u2', 'windTrack2')
    width = int(frame.shape[1] * 1)
    height = int(frame.shape[0] * 1)
    dim = (width, height)
    frame_resize = cv2.resize(frame, dim)
    img_final = frame_resize.copy()
    frame_gray = cv2.cvtColor(frame_resize, cv2.COLOR_BGR2GRAY)
    frame_bin = cv2.inRange(frame_gray, (0), (100))
    
    contours, hierarchy = cv2.findContours(frame_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    img_contour = np.zeros(frame_resize.shape, np.uint8)
    roi_bin = np.zeros(frame_gray.shape, np.uint8)
    if(len(contours)>0):
        #center_x = []
        #center_y = []
        for contour in contours:
            area_contour = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            area_rect = w*h
            if area_rect > 7300 and h > 0 and w<70:
                roi_bin[y:y+h, x:x+w] = 255
                #center_x.append(int(x+w/2))
                #center_y.append(int(y+h/2))
                #char_roi = frame_gray[y:y+h, x:x+w]
                #print("w y h are: ", w, h, area_rect)
                #showImg("char_roi", char_roi,0)     
                #cv2.rectangle(frame_resize, (x,y), (x+w,y+h),(0,255,0),2)
                cv2.drawContours(img_contour, contour, -1, (255,0,255), 1)
    roi = cv2.bitwise_and(frame_resize, frame_resize, mask= roi_bin)  
    #showImgW("frame_resize", frame_resize)
    #showImgW("img_contour", img_contour)
    showImgW("roi", roi)
    imgHSV = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    lower, upper = np.array([10, 50, 150]), np.array([30, 255, 255])
    mask1 = cv2.inRange(imgHSV, np.array(lower), np.array(upper))
    #lower, upper = np.array([80, 50, 50]), np.array([140, 255, 255]) #Mascara lineas azules
    #mask2 = cv2.inRange(imgHSV, np.array(lower), np.array(upper))
    mask = mask1
    #showImgW("mask", mask)
    kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 3))
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (6, 10))
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel1)
    #showImgW("closing1", closing)
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel2)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel2)
    #showImgW("closing", closing)
    contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    img_contour = np.zeros(frame_resize.shape, np.uint8)
    if(len(contours)>0):
        #center_x = []
        #center_y = []
        for contour in contours:
            area_contour = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            area_rect = w*h
            condicion_altura = (y+h > 136-10 and y+h < 136+10) 
            condicion_altura_salen = (y+h > 472-10 and y+h < 472+10)
            condicion_grande = w>=26 and w<=30 and h>=36 and h<=55
            condicion_mediano = w>=27 and w<=30 and h>=30 and h<=34
            condicion_pequeño = w>=18 and w<=20 and h>=29 and h<=31
            if condicion_altura:
                if np.abs(last_frame_counter - frame_counter) > 20:
                    #print('voy a contar', frame_counter)
                    if condicion_grande:
                        grandes += 1
                    elif condicion_pequeño:
                        pequeños += 1
                    elif condicion_mediano:
                        medianos += 1
                    last_frame_counter = frame_counter
            if condicion_altura_salen:
                if np.abs(last_frame_counter_salen - frame_counter) > 20:
                    if condicion_grande:  
                        grandes_salen += 1
                    elif condicion_pequeño:
                        pequeños_salen += 1
                    elif condicion_mediano:
                        medianos_salen += 1
                    last_frame_counter_salen = frame_counter
                #roi_bin[y:y+h, x:x+w] = 255
                #center_x.append(int(x+w/2))
                #center_y.append(int(y+h/2))
                #char_roi = frame_gray[y:y+h, x:x+w]
                #print("w y h are: ", w, h, area_rect, x, y)
                #showImg("char_roi", char_roi,0)     
                #cv2.rectangle(frame_resize, (x,y), (x+w,y+h),(0,255,0),2)
                cv2.drawContours(img_contour, contour, -1, (255,0,255), 1)
    total_salen = grandes_salen+medianos_salen+pequeños_salen
    total = grandes+medianos+pequeños
    porcentaje = 100
    if total > 0 and total_salen > 0:
        porcentaje = int(total_salen/total*100)
    if porcentaje <= 20 and (frame_counter%20 == 0 or (frame_counter-1)%20 == 0 or (frame_counter-2)%20 == 0 or (frame_counter-3)%20 == 0):
        cv2.circle(img_final, (210, 50), 7, (0,0,255),-1)
    else:
        pass
    cv2.circle(img_final, (210, 50), 10, (0,0,0),3)    
    cv2.putText(img_final,'Pequenas: '+str(pequeños), (10,25), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0,255), 1, cv2.LINE_AA)
    cv2.putText(img_final,'Medianas: '+str(medianos), (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0,255), 1, cv2.LINE_AA)
    cv2.putText(img_final,'Grandes: '+str(grandes), (10,75), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0,255), 1, cv2.LINE_AA)
    cv2.putText(img_final,'Total: '+str(total), (10,100), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0,255), 1, cv2.LINE_AA)
    cv2.putText(img_final,'Pequenas: '+str(pequeños_salen), (10,425), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0,255), 1, cv2.LINE_AA)
    cv2.putText(img_final,'Medianas: '+str(medianos_salen), (10,450), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0,255), 1, cv2.LINE_AA)
    cv2.putText(img_final,'Grandes: '+str(grandes_salen), (10,475), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0,255), 1, cv2.LINE_AA)
    cv2.putText(img_final,'Total: '+str(total_salen), (10,500), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0,255), 1, cv2.LINE_AA)
    cv2.putText(img_final,'Porcentaje: '+str(porcentaje)+ '%', (10,525), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0,255), 1, cv2.LINE_AA)
    
    #showImgW("img_contour", img_contour)
    showImgW("img_final", img_final)
cv2.destroyAllWindows()