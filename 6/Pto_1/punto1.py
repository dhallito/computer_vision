#By Juan David Cuscagua López
#Para filtrar los colores de las frutas, utilicé un código que hice para la actividad 2: "rangos_colores_punto1.py"
#Vale la pena descomentar todas las lines de showImg para ver el proceso de filtro
#Profe, de las mejores materias que he visto

import numpy as np
import cv2

def loadImage (path):
    imgColor = cv2.imread(path,1)
    imgGray = cv2.imread(path,0)
    return (imgColor, imgGray)

def showImg(nameWindow, matImage, t):
    cv2.imshow(nameWindow, matImage)
    cv2.waitKey(t)

if __name__ == "__main__":
    cantidad_manzanas = 0
    cantidad_cerezas = 0
    cantidad_fresas = 0
    paths = []
    for i in range(16):
        if i+1 >= 15: paths.append(str(i+1)+".jpg")
        else: paths.append(str(i+1)+".jfif") 

    for i in range(16):
        imgColor, imgGray = loadImage(paths[i])
        showImg("imgGray", imgColor, 0)
        ### Filtro Manzanas Verdes
        lower, upper = np.array([31, 93, 80]), np.array([42, 255, 243])
        imgHSV = cv2.cvtColor(imgColor, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(imgHSV, np.array(lower), np.array(upper))
        #showImg('HSV', mask, 0)
        kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(30,30))
        img_opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel1)
        #showImg("img_opening", img_opening, 0)
        img_closing = cv2.morphologyEx(img_opening, cv2.MORPH_CLOSE, kernel1)
        #showImg("img_closing", img_closing, 0)
        if 255 in img_closing:
            cantidad_manzanas += 1
            print("Hay una manzana en la imagen " + str(i+1))
        ### Filtro frutas rojas
        lower1, upper1 = np.array([0, 200, 100]), np.array([4, 255, 255])
        lower2, upper2 = np.array([176, 200, 100]), np.array([179, 255, 255])
        imgHSV = cv2.cvtColor(imgColor, cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(imgHSV, np.array(lower1), np.array(upper1))
        mask2 = cv2.inRange(imgHSV, np.array(lower2), np.array(upper2))
        mask = mask1 + mask2
        showImg('HSV', mask, 0)
        kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(20,20))
        img_opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel1)
        showImg("img_opening", img_opening, 0)
        img_closing = cv2.morphologyEx(img_opening, cv2.MORPH_CLOSE, kernel1)
        showImg("img_closing", img_closing, 0)
        if 255 in mask:
            if 255 in img_closing:
                cantidad_cerezas += 1
                print("Hay una cereza en la imagen " + str(i+1))
            else: 
                cantidad_fresas += 1
                print("Hay una fresa en la imagen " + str(i+1))
    cv2.destroyAllWindows()

    print('En total hay ' + str(cantidad_manzanas)+ ' manzanas')
    print('En total hay ' + str(cantidad_fresas)+ ' fresas')
    print('En total hay ' + str(cantidad_cerezas)+ ' cerezas')
