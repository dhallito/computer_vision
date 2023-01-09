import numpy as np
import cv2
from glob import glob
import xlsxwriter as xw

def loadImage(path):
    imgColor=cv2.imread(path,1)
    imgGray=cv2.imread(path,0)
    return imgColor, imgGray

def showImg(nameWindow, matImg):
    cv2.imshow(nameWindow,matImg)

def binImage(imgGray,u,u2):
    _ret,imgBin=cv2.threshold(imgGray,u,u2,cv2.THRESH_BINARY_INV)
    return imgBin

if __name__=='__main__':
    vectorNums=['0','1','2','3','4','5','6','7','8','9']
    countNums=[0,0,0,0,0,0,0,0,0,0]
    j=1
    row=0
    workbook=xw.Workbook('nums.xlsx')
    worksheet=workbook.add_worksheet('CaracNums')

    for i in range(0,len(vectorNums)):
        for pathImg in glob('num/'+vectorNums[i]+'/*.png'):
            imgColor, imgGray=loadImage(pathImg)
            #showImg('imgC',imgColor)
            imgBin=binImage(imgGray,0,255)

            imgBin=cv2.resize(imgBin,(25,50))
            imgColor=cv2.resize(imgColor,(25,50))
            showImg('imgBin',imgBin)

            '''
            kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
            imgErode=cv2.erode(imgBin,kernel,iterations=1) 
            showImg('imgErode',imgErode)
            '''
            cv2.waitKey(5)

            contours, hierarchy=cv2.findContours(imgBin.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
            if(len(contours)>0):
                for cnt in contours:
                    x,y,w,h = cv2.boundingRect(cnt)
                    area = w*h
                    if area>100 and w>10 and h>10:
                        countNums[i]=countNums[i]+1
                        cv2.rectangle(imgColor,(x,y),(x+w,y+h),(255,0,0),2)
                        showImg('imgColor',cv2.resize(imgColor,(125,250)))
                        cv2.waitKey(1)    

                        #Extraccion de patrones descriptivos del contorno (Escogimos unos al azar, pueden servir o no)
                        areaCnt=cv2.contourArea(cnt)    #Area del contorno
                        ar=w/h                          #Relacion de aspecto
                        p=cv2.arcLength(cnt,True)       #Perimetro
                        c=areaCnt/(pow(p,2))            #Circularidad
                        M=cv2.moments(cnt)              #Momentos de giro
                        Hu=cv2.HuMoments(M)             #Momentos de Hu
                        vectorCarac=np.array([areaCnt,ar,p,c,Hu[0][0],Hu[1][0],Hu[2][0],Hu[3][0],Hu[4][0],Hu[5][0],Hu[6][0]],dtype=np.float32)
                        
                        for carac in vectorCarac:
                            worksheet.write(row,0,i)
                            worksheet.write(row,j,carac)
                            j=j+1
                        j=1
                        row=row+1

workbook.close()
cv2.destroyAllWindows()
    

    
    