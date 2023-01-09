#By Juan David Cuscagua

import numpy as np
import cv2

path = input('Ingrese el path con la extensión: ')

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
        if x < 0: x = 0
        if y < 0: y = 0
        x1=x
        y1=y
    if(event == cv2.EVENT_LBUTTONUP):
        if x < 0: x = 0
        if y < 0: y = 0
        x2=x
        y2=y
        bandRoi=True

def nothing(x):
    pass

cv2.namedWindow('Limite_superior')
cv2.createTrackbar('u1', 'Limite_superior', 0, 255, nothing)        # u1 = umbral

cv2.namedWindow('Limite_inferior')
cv2.createTrackbar('u2', 'Limite_inferior', 0, 255, nothing)        # u2 = umbral

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
    roi_gray = imgGray
    resized_roi = imgColor
    resized_roi_gray = imgGray
    while True:
        if (cv2.waitKey(1) & 0xFF == 13):
            break
        u1 = cv2.getTrackbarPos('u1', 'Limite_superior')
        u2 = cv2.getTrackbarPos('u2', 'Limite_inferior')
        showImgW("imgColor", imgColor)
        if bandRoi == True:
            print(x1, y1)
            print(x2, y2)
            bandRoi = False
            if y2<y1 and x2<x1:
                roi=imgColor[y2:y1, x2:x1]
                roi_gray=imgGray[y2:y1, x2:x1]
            elif y2<y1 and x1<x2:
                roi=imgColor[y2:y1, x1:x2]
                roi_gray=imgGray[y2:y1, x1:x2]
            elif y1<y2 and x1<x2:
                roi=imgColor[y1:y2, x1:x2]
                roi_gray=imgGray[y1:y2, x1:x2]
            elif y1< y2 and x2<x1:
                roi=imgColor[y1:y2, x2:x1]
                roi_gray=imgGray[y1:y2, x2:x1]
            width = int(roi.shape[1] * 10)
            height = int(roi.shape[0] * 10)
            dim = (width, height)
            resized_roi = cv2.resize(roi, dim, interpolation = cv2.INTER_AREA)
            resized_roi_gray = cv2.resize(roi_gray, dim, interpolation = cv2.INTER_AREA)
            showImgW("Zoom x10", resized_roi)
            showImgW("Zoom x10 gray", resized_roi_gray)
        _red, imgTozero = cv2.threshold(resized_roi_gray, u1, 255, cv2.THRESH_TOZERO_INV)
        _red, imgBinary = cv2.threshold(imgTozero, u2, 255, cv2.THRESH_BINARY)
        showImgW("imgBinary_inRange", imgBinary)
    cv2.destroyAllWindows()