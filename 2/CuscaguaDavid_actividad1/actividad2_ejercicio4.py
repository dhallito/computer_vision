#by Juan David Cuscagua López

from functools import total_ordering
from re import A
import numpy as np
import cv2

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
    for i in range(rows_size):
        for j in range(columns_size):
            if i > rows_size/2:
                if j > columns_size/2:
                    imgNew[i,j,0] = 0
                    imgNew[i,j,1] = 0 
                else:
                    imgNew[i,j,0] = 0
                    imgNew[i,j,2] = 0 
            else:
                if j > columns_size/2:
                    imgNew[i,j,1] = 0
                    imgNew[i,j,2] = 0                 
    while True:
        showImgW("imgOriginal", imgOriginal)
        showImgW("imgNew", imgNew)
        if (cv2.waitKey(1) & 0xFF == ord ('q')):
            break