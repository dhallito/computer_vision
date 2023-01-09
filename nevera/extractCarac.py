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
    _ret,imgBin=cv2.threshold(imgGray,u,u2,cv2.THRESH_BINARY)
    return imgBin

if __name__=='__main__':
    vectorNums=['aguacatico','compota','juguito','limoncito','maltica','manzanita', 'vacio']
    countNums=[0,0,0,0,0,0,0]
    j=1
    row=0
    workbook=xw.Workbook('alimentos.xlsx')
    worksheet=workbook.add_worksheet('CaracAlimentos')

    for i in range(0,len(vectorNums)):
        for pathImg in glob('alimentos/'+vectorNums[i]+'/*.jpg'):
            imgColor, imgGray=loadImage(pathImg)
            #showImg('imgC',imgColor)
            imgBin=cv2.resize(imgGray,(25,50))
            imgColor=cv2.resize(imgColor,(25,50))
            #imgBin=binImage(imgBin,5,255)
            #showImg('imgColor',imgColor)
            
            #kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
            #imgOpening=cv2.morphologyEx(imgBin,cv2.MORPH_OPEN,kernel)
            #imgClosing=cv2.morphologyEx(imgOpening,cv2.MORPH_CLOSE,kernel)
            #showImg('imgClosing',imgClosing)
            
            #cv2.waitKey(0)

            countNums[i]=countNums[i]+1
            vector_pixel = []
            for a in imgColor:
                for b in a:
                    for c in b:
                        vector_pixel.append(c)
            vectorCarac=np.array(vector_pixel,dtype=np.float32)
                        
            for carac in vectorCarac:
                worksheet.write(row,0,i)
                worksheet.write(row,j,carac)
                j=j+1
            j=1
            row=row+1
            

            '''contours, hierarchy=cv2.findContours(imgBin.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
            if(len(contours)>0):
                for cnt in contours:
                    x,y,w,h = cv2.boundingRect(cnt)
                    area = w*h
                    if area>100 and w>10 and h>40:
                        countNums[i]=countNums[i]+1
                        #cv2.rectangle(imgColor,(x,y),(x+w,y+h),(255,0,0),2)
                        #cv2.drawContours(imgColor, cnt, -1, (255,0,255), 1)
                        #showImg('imgColor',cv2.resize(imgColor,(125,250)))
                        #showImg('imgClosing',cv2.resize(imgClosing,(125,250)))
                        #cv2.waitKey(0)    

                        #Extraccion de patrones descriptivos del contorno (Escogimos unos al azar, pueden servir o no)
                        areaCnt=cv2.contourArea(cnt)    #Area del contorno
                        ar=w/h                          #Relacion de aspecto
                        p=cv2.arcLength(cnt,True)       #Perimetro
                        c=areaCnt/(pow(p,2))            #Circularidad
                        M=cv2.moments(cnt)              #Momentos de giro
                        Hu=cv2.HuMoments(M)             #Momentos de Hu
                        Li = cv2.fitLine(cnt, cv2.DIST_L2, 0, 0.01, 0.01)   #Fitting a Line
                        area_p = areaCnt/p              #Relación area perímetro
                        k = int(cv2.isContourConvex(cnt))   #Checking Convexity
                        extent = areaCnt/(w*h)                           #Extension
                        (xcircle,ycircle),radius = cv2.minEnclosingCircle(cnt)
                        ellipse = cv2.fitEllipse(cnt)
                        xcenterE = ellipse[0][0]
                        ycenterE = ellipse[0][1]
                        rotationE = ellipse[2]
                        widthE = ellipse[1][0]
                        heightE = ellipse[1][1]

                        vectorCarac=np.array([  areaCnt,
                                                ar,
                                                p,
                                                c,
                                                Hu[0][0],Hu[1][0],Hu[2][0],Hu[3][0],Hu[4][0],Hu[5][0],Hu[6][0],
                                                Li[0][0],Li[1][0],Li[2][0],Li[3][0],
                                                area_p,
                                                k,
                                                extent,
                                                xcircle,
                                                ycircle,
                                                radius,
                                                xcenterE,
                                                ycenterE,
                                                rotationE,
                                                widthE,
                                                heightE] ,dtype=np.float32)
                        
                        -----------------COCO------------------------
                        areaCnt=cv2.contourArea(cnt)    #Area del contorno
                        ar=w/h                          #Relacion de aspecto
                        p=cv2.arcLength(cnt,True)       #Perimetro
                        c=areaCnt/(pow(p,2))            #Circularidad
                        M=cv2.moments(cnt)              #Momentos de giro
                        Hu=cv2.HuMoments(M)             #Momentos de Hu
                        (x1,y1),(MA,ma),angle = cv2.fitEllipse(cnt)     #Orientacion
                        equi_diameter = np.sqrt(4*areaCnt/np.pi)        #Diametro equivalente 
                        rel_area=areaCnt/area
                        leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
                        rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
                        topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
                        bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
                        hull = cv2.convexHull(cnt)
                        hull_area = cv2.contourArea(hull)
                        solidity = float(areaCnt)/hull_area
                        
                        vectorCarac=np.array([  areaCnt,
                                                p,
                                                c,
                                                Hu[0][0],Hu[1][0],Hu[2][0],Hu[3][0],Hu[4][0],Hu[5][0],Hu[6][0],
                                                angle,
                                                MA,
                                                ma,
                                                x1,
                                                y1,
                                                equi_diameter,
                                                rel_area,
                                                leftmost[1],
                                                rightmost[1],
                                                topmost[0],
                                                bottommost[0],
                                                hull_area,
                                                solidity],dtype=np.float32)

                        for carac in vectorCarac:
                            worksheet.write(row,0,i)
                            worksheet.write(row,j,carac)
                            j=j+1
                        j=1
                        row=row+1'''

workbook.close()
cv2.destroyAllWindows()