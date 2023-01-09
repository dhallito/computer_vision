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
    imgColorBlue, imgGray = loadImage(path)
    imgColorGreen, imgGray = loadImage(path)
    imgColorRed, imgGray = loadImage(path)
        
    imgColorBlue[:,:,1] = 0
    imgColorBlue[:,:,2] = 0

    imgColorGreen[:,:,0] = 0
    imgColorGreen[:,:,2] = 0

    imgColorRed[:,:,0] = 0
    imgColorRed[:,:,1] = 0

    while True:
        showImgW("imgColor", imgColor)
        showImgW("imgColorBlue", imgColorBlue)
        showImgW("imgColorGreen", imgColorGreen)
        showImgW("imgColorRed", imgColorRed)
        if (cv2.waitKey(1) & 0xFF == ord ('q')):
            break
        
    cv2.destroyAllWindows()


    