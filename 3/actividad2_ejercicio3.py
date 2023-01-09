#by Juan David Cuscagua López
from functools import total_ordering
from re import A
import numpy as np
import cv2
from statistics import mode

path = "barras.png"

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
    _red, imgBinary = cv2.threshold(imgGray, 60, 255, cv2.THRESH_BINARY)
    
    showImg("imgBinary", imgBinary,0)
    cv2.destroyAllWindows()

    conteo = []
    anchos = []

    for i in range(len(imgBinary)):
            array_ranges = []
            last_pos_final = 0
            for j in range(len(imgBinary[i])):
                if imgBinary[i,j] == 255:
                    if j > last_pos_final:    
                        aux_pos_inicial = j
                        aux_pos_final = j
                        while imgBinary[i, aux_pos_final] == 255:
                            aux_pos_final += 1
                        array_ranges.append([aux_pos_inicial, aux_pos_final])
                        last_pos_final = aux_pos_final
            conteo.append(len(array_ranges))
            anchos.append(array_ranges)

    total = mode(conteo)
    distancia_entre_barras = []
    for i in range(total):
        distancia_entre_barras.append([0,0])
    contar = 0

    for i in anchos:
        if len(i) == total:
            contar += 1
            for j in range(total):
                distancia_entre_barras[j][0]+= i[j][0]
                distancia_entre_barras[j][1]+= i[j][1]

    for j in range(total):
                distancia_entre_barras[j][0]= distancia_entre_barras[j][0]/contar
                distancia_entre_barras[j][1]= distancia_entre_barras[j][1]/contar   

    distancia_entre_barras_final = []
    for k in range(len(distancia_entre_barras)-1):
        distancia = distancia_entre_barras[k+1][0] - distancia_entre_barras[k][1]
        distancia_entre_barras_final.append(distancia)
        
    print('Total de barras: '+ str(total))

    print('\nPosiciones: ' + str(distancia_entre_barras))
    print('\nDistancias entre barras: ' + str(distancia_entre_barras_final))