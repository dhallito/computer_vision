#by Juan David Cuscagua López

#Con ROIs, se identifican las distancias máximas entre monedas y se pone un valor aproximado de d^2=80

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
    
    showImg("imgBinary", imgBinary,0)
    cv2.destroyAllWindows()

    contador = 0
    array_monedas = []
    for i in range(len(imgBinary)):
        for j in range(len(imgBinary)):
            if imgBinary[i,j] == 0:
                contador += 1
                is_near = False
                for k in range(len(array_monedas)):
                    for l in range(len(array_monedas[len(array_monedas)-1-k])):
                        if (array_monedas[len(array_monedas)-1-k][l][0]-i)**2 + (array_monedas[len(array_monedas)-1-k][l][1]-j)**2 < 80:
                            is_near = True
                            array_monedas[k].append([i,j])
                            break
                        pass
                    if is_near == True:
                        break
                if is_near == False:
                    array_monedas.append([[i,j]])
    print('El número de monedas presente en la imagen es ' + str(len(array_monedas)))
    print('El tamaño promedio de las monedas en la imagen es de ' + str(contador/len(array_monedas)) + ' pixeles')