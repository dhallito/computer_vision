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
    
    #showImg("imgBinary", imgBinary,0)
    #cv2.destroyAllWindows()

    array_pos_central = []
    last_array_ranges = []
    for i in range(len(imgBinary)):
        array_ranges = []
        last_pos_final = 0
        for j in range(len(imgBinary[i])):
            if imgBinary[i,j] == 0:
                if j > last_pos_final:    
                    aux_pos_inicial = j
                    aux_pos_final = j
                    while imgBinary[i, aux_pos_final] == 0:
                        aux_pos_final += 1
                    array_ranges.append([aux_pos_inicial, aux_pos_final])
                    last_pos_final = aux_pos_final
        if (len(last_array_ranges) == len(array_ranges)) and len(last_array_ranges)>0:
            for k in range(len(last_array_ranges)):
                if last_array_ranges[k][1] - last_array_ranges[k][0] > array_ranges[k][1]-array_ranges[k][0]:
                    ##encontré un centro
                    array_pos_central.append([i,(array_ranges[k][1]+array_ranges[k][0])/2])
        last_array_ranges = array_ranges


    for i in range(len(array_pos_central)):
        for j in range(len(array_pos_central)-i-1):
            if np.abs(array_pos_central[i][1] - array_pos_central[j+i+1][1]) < 20 and np.abs(array_pos_central[i][0] - array_pos_central[j+i+1][0]) < 20:
                array_pos_central[i+j+1][0]=0
                array_pos_central[i+j+1][1]=0
            pass
    
    print(array_pos_central)

                
    


   
   
    
    '''total_pixel = 0
    
    for i in range(len(imgBinary)):
        for j in range(len(imgBinary[i])):
            if imgBinary[i,j] == 0:
                total_pixel += 1
            pass



    print(total_pixel)'''
