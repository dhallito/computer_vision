#by Juan David Cuscagua López

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

if __name__ == "__main__":
    paths = []
    for i in range(5): 
        paths.append("blister_"+str(i+1)+".jpg")
    for path in paths: 
        imgColor, imgGray = loadImage(path)
        lower, upper = np.array([16, 50, 150]), np.array([22, 255, 255])
        imgHSV = cv2.cvtColor(imgColor, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(imgHSV, np.array(lower), np.array(upper))
        showImg('imgColor', imgColor, 0)  
        print("--------------------------------------")
        print("Imagen", path)
        faltantes = 0
        for i in range(4):
            for j in range(3):
                if 255 in mask[15+int((180-15)/4)*(i):15+int((180-15)/4)*(i+1), 15+int((315-15)/3)*(j):15+int((315-15)/3)*(j+1)]:
                    #print("Pastilla en la posicion ", str(i+1), str(j+1))
                    pass
                else:
                    faltantes += 1
                    print("Falta pastilla en la fila", str(i+1), "de la columna", str(j+1))
        if faltantes == 0:
            print("No faltan pastillas")
        else:
            print("Faltan", str(faltantes), "pastillas")
        showImg('HSV', mask, 0)
        

