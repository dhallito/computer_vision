from sys import path_importer_cache
import cv2
import numpy as np
import joblib

model_pca = joblib.load('model_pca.pkl')
model_ss = joblib.load('model_ss.pkl')
model_mlp = joblib.load('model_mlp.pkl')

pathImg = "num/8/8 (1).png"
 
imgGray = cv2.imread(pathImg,0)
imgColor = cv2.imread(pathImg,1)
ret, imgBin = cv2.threshold(imgGray,0,255,
                            cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
imgBinResize = cv2.resize(imgBin, (25,50))
imgColorResize = cv2.resize(imgColor, (25,50))
cv2.imshow("imgBinResize", imgBinResize)
cv2.waitKey(1)
 
contours,hierarchy = cv2.findContours(imgBinResize.copy(), \
                                            cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
 
for cnt in contours:
    x,y,w,h = cv2.boundingRect(cnt)
    area = w*h
    if(area>100 and w>10 and h>10):
        cv2.rectangle(imgColorResize,
                        (x,y), (x+w, y+h),(255,0,0),2)
        cv2.imshow("imgColorResize",
                    cv2.resize(imgColorResize, (125,250)))
        cv2.waitKey(0)
 
        #extrayendo patrones descriptivos de mi contorno
        areaCnt = cv2.contourArea(cnt)
        ar = w/h
        p = cv2.arcLength(cnt,True)
        c = areaCnt/(pow(p,2))
        M = cv2.moments(cnt)
        Hu = cv2.HuMoments(M)
        vectorCarac = np.array([areaCnt, ar, p, c,
                                Hu[0][0], Hu[1][0],
                                Hu[2][0], Hu[3][0],
                                Hu[4][0], Hu[5][0],
                                Hu[6][0]],
                                dtype = np.float32)
        vc_r = vectorCarac.reshape(1, -1)
        vc_ss = model_ss.transform(vc_r)
        vc_psa = model_pca.transform(vc_ss)
        result_predict = model_mlp.predict(vc_psa)
        print(result_predict)

