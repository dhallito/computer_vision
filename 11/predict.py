from sys import path_importer_cache
import cv2
import numpy as np
import joblib

model_pca = joblib.load('model_pca.pkl')
model_ss = joblib.load('model_ss.pkl')
model_mlp = joblib.load('model_mlp.pkl')

def decodificar(argument):
    switcher = {
        0: "A",
        1: "B",
        2: "C",
        3: "D",
        4: "E",
        5: "F",
        6: "G",
        7: "H",
        8: "I",
        9: "P",
        10: "R",
        11: "S",
        12: "T",
        13: "V",
        14: "X",
        15: "Z"
    }
    return(switcher.get(argument, "Invalid month"))

pathImg = "Test/test_all/all.png"
 
imgGray = cv2.imread(pathImg,0)
imgColor = cv2.imread(pathImg,1)
ret, imgBin = cv2.threshold(imgGray,0,255,
                            cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imshow("imgBin", imgBin)
cv2.waitKey(0)

letras = []
letras_carac = []

contours,hierarchy = cv2.findContours(imgBin.copy(), \
                                            cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

for cnt in contours:
    x,y,w,h = cv2.boundingRect(cnt)
    area = w*h
    if(area>100 and w>10 and h>10):
        '''cv2.rectangle(imgColor,
                        (x,y), (x+w, y+h),(255,0,0),2)
        cv2.imshow("imgColor", imgColor)'''
        char_roi = imgBin[y:y+h, x:x+w]
        char_roi_resisze = cv2.resize(char_roi, (25,50))
        letras.append(char_roi_resisze)
        letras_carac.append([x,y,w,h])
        '''cv2.imshow("char_roi_resize", char_roi_resisze)
        cv2.imshow("char_roi", char_roi)
        cv2.waitKey(0)'''
letras_predict = []
for letra in letras:
    #cv2.imshow("letra", letra)
    contours,hierarchy = cv2.findContours(letra.copy(), \
                                            cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        area = w*h
        if area>100 and w>20 and h>30:
            #extrayendo patrones descriptivos de mi contorno
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
            vectorCarac=np.array([  areaCnt,
                                    #ar,
                                    p,
                                    c,
                                    Hu[0][0],Hu[1][0],Hu[2][0],Hu[3][0],Hu[4][0],Hu[5][0],Hu[6][0],
                                    Li[0][0],Li[1][0],Li[2][0],Li[3][0],
                                    area_p,
                                    k,
                                    #extent
                                    ],dtype=np.float32)
            vc_r = vectorCarac.reshape(1, -1)
            vc_ss = model_ss.transform(vc_r)
            vc_psa = model_pca.transform(vc_ss)
            result_predict = model_mlp.predict(vc_psa)
            letras_predict.append(decodificar(result_predict[0]))
            
    #cv2.waitKey(0)

img_final = imgColor.copy()
for i in range(len(letras)):
    x = letras_carac[i][0]
    y = letras_carac[i][1]
    w = letras_carac[i][2]
    h = letras_carac[i][3]
    cv2.putText(img_final, letras_predict[i], (int(x+w/2), int(y+h+30)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
cv2.imshow("img_final", img_final)
cv2.waitKey(0)
cv2.destroyAllWindows()