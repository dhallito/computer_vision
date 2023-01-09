#by Juan David Cuscagua López

from functools import total_ordering
from re import A
import numpy as np
import cv2
from math import floor

path = "delfin.jpg"

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
    rows_size = len(imgColor)
    columns_size = len(imgColor[0])
    imgOriginal = np.array(imgColor)
    imgNew = np.array(imgOriginal)
    n = int(input('Ingrese el numero n: '))
    for i in range(n):
        for j in range(n):
            imgNew[floor(i*rows_size/n):,floor(j*columns_size/n):]=imgOriginal[floor(i*rows_size/n):,floor(j*columns_size/n):]
            if (j+i%3)%3 == 0:
                imgNew[floor(i*rows_size/n):,floor(j*columns_size/n):,1] = 0
                imgNew[floor(i*rows_size/n):,floor(j*columns_size/n):,2] = 0
            elif (j+i%3)%3 == 1:
                imgNew[floor(i*rows_size/n):,floor(j*columns_size/n):,0] = 0
                imgNew[floor(i*rows_size/n):,floor(j*columns_size/n):,2] = 0
            elif (j+i%3)%3 == 2:
                imgNew[floor(i*rows_size/n):,floor(j*columns_size/n):,0] = 0
                imgNew[floor(i*rows_size/n):,floor(j*columns_size/n):,1] = 0
    while True:
        showImgW("imgOriginal", imgOriginal)
        showImgW("imgNew", imgNew)
        if (cv2.waitKey(1) & 0xFF == ord ('q')):
            break