#by Juan David Cuscagua López
#Seleccione todos los ROIs manualmente, luego, oprima enter y apareceran todos a la ver en la pantalla.

import numpy as np
import cv2

path = 'nebulosa.jpg'

def loadImage (path):
    imgColor = cv2.imread(path,1)
    imgGray = cv2.imread(path,0)
    return (imgColor, imgGray)

def showImg(nameWindow, matImage, t):
    cv2.imshow(nameWindow, matImage)
    cv2.waitKey(t)

def showImgW(nameWindow, matImage):
    cv2.imshow(nameWindow, matImage)

def nothing(x):
    pass

def mouseClick(event, x, y, flags, param):
    global x1, x2, y1, y2, bandRoi
    if(event == cv2.EVENT_LBUTTONDOWN):
        x1=x
        y1=y
    if(event == cv2.EVENT_LBUTTONUP):
        x2=x
        y2=y
        bandRoi=True
        
cv2.namedWindow("imgColor")
cv2.setMouseCallback("imgColor", mouseClick)

if __name__ == "__main__":
    imgColor, imgGray = loadImage(path)
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    bandRoi = False
    roi = imgColor
    roi_array = []
    while True:
        if (cv2.waitKey(1) & 0xFF == 13):
            break
        showImgW("imgColor", imgColor)
        if bandRoi == True:
            print(x1, y1)
            print(x2, y2)
            bandRoi = False
            if y2<y1 and x2<x1:
                roi=imgColor[y2:y1, x2:x1]
            elif y2<y1 and x1<x2:
                roi=imgColor[y2:y1, x1:x2]
            elif y1<y2 and x1<x2:
                roi=imgColor[y1:y2, x1:x2]
            elif y1< y2 and x2<x1:
                roi=imgColor[y1:y2, x2:x1]
            roi_array.append(roi)
            showImgW("imgColorRoi", roi)
    cv2.destroyAllWindows()
    if len(roi_array) > 0:
        for i in range(len(roi_array)):
                showImgW("imgColorRoi " + str(i), roi_array[i])
        while True:
            if (cv2.waitKey(1) & 0xFF == ord ('q')):
                break
    cv2.destroyAllWindows()