#by Juan David Cuscagua López

## NOTA: PARA CAMBIAR EL COLOR DE LA FACHADA, MOVER LA BARRA Y LUEGO DAR ENTER

import numpy as np
import cv2

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

def get_color_range(imgColor):
    global x1, x2, y1, y2, bandRoi
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
            roi_array[i] = cv2.cvtColor(roi_array[i], cv2.COLOR_BGR2HSV)
        h_array = []
        s_array = []
        v_array = []
        for i in roi_array:
            for j in i:
                for k in j:
                    h_array.append(k[0])
                    s_array.append(k[1])
                    v_array.append(k[2])

        return [min(h_array), min(s_array), min(v_array)], [max(h_array), max(s_array), max(v_array)]
    else:
        return 0, 0


cv2.namedWindow("imgColor")
cv2.setMouseCallback("imgColor", mouseClick)

cv2.namedWindow('windTrack1')
cv2.createTrackbar('u1', 'windTrack1', 0, 179, nothing)        # u1 = umbral

if __name__ == "__main__":
    path = 'casita.jpg'
    imgColor, imgGray = loadImage(path)
    showImgW('imgColor', imgColor)
    #lower, upper = get_color_range(imgColor) #Obtiene el rango HSV de color mediante ROIs
    #print(lower, upper)
    lower, upper = np.array([14, 107, 100]), np.array([25, 255, 255])
    imgHSV = cv2.cvtColor(imgColor, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV, np.array(lower), np.array(upper))
    #showImg('HSV', mask, 0)
    imgNewColor = imgColor
    while True:
        if (cv2.waitKey(1) & 0xFF == ord ('q')):
            break
        if (cv2.waitKey(1) & 0xFF == 13):
            imgNewColor = imgHSV
            for i in range(len(imgNewColor)):
                for j in range(len(imgNewColor[i])):
                    if mask[i,j] == 255:
                        imgNewColor[i, j, 0] = u1
            imgNewColor = cv2.cvtColor(imgNewColor, cv2.COLOR_HSV2BGR)
        u1 = cv2.getTrackbarPos('u1', 'windTrack1')
        showImgW("imgNewColor", imgNewColor)
    cv2.destroyAllWindows()