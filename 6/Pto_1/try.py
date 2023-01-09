#Date: 20/08/2022 - Quiz 1

from json import load
import cv2 
import numpy as np

path = 'D:\Documentos\semestre_10\vision_artificial\Quiz\Quiz1\Images\Pto_1'
path = 'D:/Documentos\semestre_10/vision_artificial/Quiz/Quiz1/Images/Pto_1'

def loadImage(path):
    imgColor = cv2.imread(path,1)
    imgGray = cv2.imread(path,0)
    return imgColor,imgGray

def showImg(nameWindow, matImg , t):
    cv2.imshow(nameWindow, matImg)
    cv2.waitKey(t)

def showImgW(nameWindow, matImg):
    cv2.imshow(nameWindow, matImg)

def findFruit(maskGreen,maskRed):
    fruit = [0,0,0]
    minRed = 1000
    minApple = 5000
    minStrawberry = 100
    zerosGreen = cv2.countNonZero(maskGreen)
    zerosRed = cv2.countNonZero(maskRed)

    if (zerosGreen > minApple):
        fruit[0] = fruit[0] + 1 
    if(zerosRed>minRed):
        kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT,(49,1))
        maskRed = cv2.erode(maskRed,kernel1,iterations=2)
        zerosStrawberry= cv2.countNonZero(maskRed)
        if(zerosStrawberry>minStrawberry):
            fruit[1] = fruit[1] + 1 
        else:
            fruit[2] = fruit[2] + 1 

    return fruit

if __name__ == "__main__":
    for i in range(1,17):
        allPath = '%s/%d.jfif' % (path,i)
        print(allPath)
        imgColor, imgGray = loadImage(allPath)
        imgHSV = cv2.cvtColor(imgColor,cv2.COLOR_BGR2HSV)

        low_apple= np.array([30,70,50])
        high_apple = np.array([70,255,255])
        apple_mask= cv2.inRange(imgHSV, low_apple, high_apple)
        

        umbral_bajo1 = np.array([0,50,100])
        umbral_alto1 = np.array([10,255,255])

        umbral_bajo2 = np.array([170,50,100])
        umbral_alto2 = np.array([179,255,255])

        mask1 = cv2.inRange(imgHSV,umbral_bajo1,umbral_alto1)
        mask2 = cv2.inRange(imgHSV,umbral_bajo2,umbral_alto2)

        srawberry_mask = cv2.add(mask1,mask2)
        


        fruit = findFruit(apple_mask,srawberry_mask)
        print(fruit)
        showImg('imgColor',imgColor,0)

    cv2.destroyAllWindows()