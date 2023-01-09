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


#capture = cv2.VideoCapture(0) #ip o extension
#capture = cv2.VideoCapture("up&up.mp4")

'''while(capture.isOpened()):
    ret, frame = capture.read()
    showImgW("frame", frame)
    if (cv2.waitKey(1) & 0xFF == ord ('q')) or ret==False:
            break'''

url = 'http://192.168.246.125:8080/shot.jpg'
while True:
    #u1 = cv2.getTrackbarPos('u1', 'windTrack1')
    #u2 = cv2.getTrackbarPos('u2', 'windTrack2')
    img_url = urllib.request.urlopen(url)
    img_np = np.array(bytearray(img_url.read()), dtype=np.uint8)
    frame = cv2.imdecode(img_np, -1)
    frame_resize = cv2.resize(frame,(640,480))
    frame_gray = cv2.cvtColor(frame_resize, cv2.COLOR_BGR2GRAY)
    #_red, frame_tozero = cv2.threshold(frame_gray, 36, 255, cv2.THRESH_TOZERO_INV)
    #_red, frame_bin = cv2.threshold(frame_tozero, 0, 255, cv2.THRESH_BINARY)
    frame_bin = cv2.inRange(frame_gray, (0), (36))
    contours, hierarchy = cv2.findContours(frame_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    img_contour = np.zeros(frame_resize.shape, np.uint8)
    if(len(contours)>0):
        for contour in contours:
            area_contour = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            area_rect = w*h
            if area_rect > 10 and area_rect < 600 and h > 10 and w>3:
                cv2.rectangle(frame_resize, (x,y), (x+w,y+h),(0,255,0),2)
                cv2.drawContours(img_contour, contour, -1, (255,0,255), 1)
                char_roi = frame_gray[y:y+h, x:x+w]
                showImg("char_roi", char_roi,0)
                #print("w y h are: ", w, h, area_rect)
                #cv2.waitKey(0)


            

    #showImgW("frame_tozero", frame_tozero)
    showImgW("img_contour", img_contour)
    #showImgW("frame_bin", frame_bin)
    showImgW("frame_resize", frame_resize)
    
    if (cv2.waitKey(30) & 0xFF == ord ('q')):
            break


cv2.destroyAllWindows()

    
