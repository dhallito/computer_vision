#by Juan David Cuscagua López

#Usando TrackBar defino limites:
#Limite superior 200
#Limite 121
#Limite 88

from functools import total_ordering
from re import A
import numpy as np
import cv2

path = "monedas.jpg"

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

if __name__ == "__main__":
    imgColor, imgGray = loadImage(path)
    u_fondo = 200
    _red, imgBinary = cv2.threshold(imgGray, u_fondo, 255, cv2.THRESH_BINARY)
    imgNewColor = imgColor
    randomColor1 = np.random.randint(256, size=3)
    randomColor2 = np.random.randint(256, size=3)
    randomColor3 = np.random.randint(256, size=3)
    for i in range(len(imgGray)):
        for j in range(len(imgGray[i])):
            if imgGray[i,j] > 200:
                imgNewColor[i,j] = [255,255,255]
            elif imgGray[i,j] > 121:
                imgNewColor[i,j] = randomColor1
            elif imgGray[i,j] > 88:
                imgNewColor[i,j] = randomColor2
            else:
                imgNewColor[i,j] = randomColor3
    showImg("imgNewColor", imgNewColor,0)
    cv2.destroyAllWindows()