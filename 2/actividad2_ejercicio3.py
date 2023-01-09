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
    imgNew = np.empty_like(imgOriginal)
    for i in range(rows_size):
        for j in range(columns_size):
            imgNew[i,j] = imgOriginal[rows_size-1-i,j]

    while True:
        showImgW("imgOriginal", imgOriginal)
        showImgW("imgNew", imgNew)
        if (cv2.waitKey(1) & 0xFF == ord ('q')):
            break
