from itertools import count
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

cv2.namedWindow('windTrack1')
cv2.createTrackbar('u1', 'windTrack1', 0, 255, nothing)        # u1 = umbral

cv2.namedWindow('windTrack2')
cv2.createTrackbar('u2', 'windTrack2', 0, 255, nothing)        # u2 = umbral

capture = cv2.VideoCapture("codo.mp4")

img_trayectoria = np.zeros((576,324,3), np.uint8)
centros = []

while(capture.isOpened()):
    ret, frame = capture.read()
    if (cv2.waitKey(50) & 0xFF == ord ('q')) or ret==False:
            break
    u1 = cv2.getTrackbarPos('u1', 'windTrack1')
    u2 = cv2.getTrackbarPos('u2', 'windTrack2')
    width = int(frame.shape[1] * 0.3)
    height = int(frame.shape[0] * 0.3)
    dim = (width, height)
    frame_resize = cv2.resize(frame, dim)
    color_mask = frame_resize.copy()
    lower, upper = np.array([25, 180, 100]), np.array([32, 255, 255])
    imgHSV = cv2.cvtColor(frame_resize, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(imgHSV, np.array(lower), np.array(upper))
    lower, upper = np.array([70, 50, 50]), np.array([130, 255, 255])
    mask2 = cv2.inRange(imgHSV, np.array(lower), np.array(upper))
    mask = mask1 + mask2
    color_mask = cv2.bitwise_and(frame_resize, frame_resize, mask= mask)
    _red, mask_inverse = cv2.threshold(mask, 100, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    img_contour = np.zeros(color_mask.shape, np.uint8)
    if(len(contours)>0):
        center_x = []
        center_y = []
        for contour in contours:
            area_contour = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            area_rect = w*h
            if area_rect > 50 and area_rect < 1000 and h > 0 and w>0:
                center_x.append(int(x+w/2))
                center_y.append(int(y+h/2))
                #cv2.rectangle(frame_resize, (x,y), (x+w,y+h),(0,255,0),2)
                cv2.drawContours(img_contour, contour, -1, (255,0,255), 1)
                #char_roi = frame_gray[y:y+h, x:x+w]
                #showImg("char_roi", char_roi,0)
                #print("w y h are: ", w, h, area_rect)
                #cv2.waitKey(0)
        cv2.line(img_contour, (center_x[0], center_y[0]), (center_x[1], center_y[1]), (0,255,0), 1)
        distancia = np.sqrt((center_x[0]-center_x[1])**2 + (center_y[0]-center_y[1])**2)
        angulo = np.rad2deg(np.arctan((center_y[0]-center_y[1])/(center_x[0]-center_x[1]+.00001)))
        cv2.circle(img_trayectoria, (center_x[0], center_y[0]), 3, (255,0,0),-1)
        cv2.circle(img_trayectoria, (center_x[1], center_y[1]), 3, (0,0,255),-1)
        '''img_trayectoria[center_y[0], center_x[0]] = [0,255,0]
        img_trayectoria[center_y[1], center_x[1]] = [255,0,0]'''
    cv2.putText(img_contour,'Distancia: '+str(distancia), (10,450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
    cv2.putText(img_contour,'Angulo: '+str(angulo)+'°', (10,500), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
    img_final = cv2.add(img_trayectoria, img_contour)
    '''color_mask[:,:,0] = cv2.add(color_mask[:,:,0], mask_inverse)
    color_mask[:,:,1] = cv2.add(color_mask[:,:,1], mask_inverse)
    color_mask[:,:,2] = cv2.add(color_mask[:,:,2], mask_inverse)'''
    '''for i in range(len(frame_resize)):
        for j in range(len(frame_resize[0])):
            if mask[i,j] == 0:
                color_mask[i,j] = [0, 0, 0]'''
    showImgW("img", img_final)

cv2.destroyAllWindows()