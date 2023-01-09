#by Juan David Cuscagua López
#Mediante rois se identifican rangos de colores en base HSV

## NOTA: Se utilizó este codigo para sacar rangos de colores 
# Rango Verde Manzana: Para las imagenes 1-5
# [38, 180, 133] [42, 255, 226]
# [31, 105, 152] [38, 246, 236]
# [31, 177, 79] [39, 255, 174]
# [36, 150, 123] [40, 253, 211]
# [36, 93, 160] [40, 255, 243]
# Maximos y minimos = [31, 93, 80] [42, 255, 243] 

# Rango Rojo Cereza: Como se compone de dos conjuntos aislados, se utiliza la referencia de rango 
# de colores desde internet, pero los valores de Saturación y Valor se obtienen de igual forma para las imagenes 11-14
# [-, 137, 72] [-, 248, 182]
# [-, 41, 133] [-, 255, 242]
# [-, 148, 88] [-, 255, 217]
# [-, 53, 188] [-, 251, 253]
# Máximos y mínimos = [-, 41, 72] [-, 255, 253]

# LOS RANGOS SE ALTERARON A BENEFICIO DE LA SELECCIÓN

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

if __name__ == "__main__":
    path = '11.jfif'
    imgColor, imgGray = loadImage(path)
    showImgW('imgColor', imgColor)
    lower, upper = get_color_range(imgColor) #Obtiene el rango HSV de color mediante ROIs
    print(lower, upper)
    imgHSV = cv2.cvtColor(imgColor, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV, np.array(lower), np.array(upper))
    showImg('HSV', mask, 0)
    