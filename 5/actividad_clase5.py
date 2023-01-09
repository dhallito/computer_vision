#by Juan David Cuscagua López

import numpy as np
import cv2

path = "barras_cir.png"

def loadImage (path):
    imgColor = cv2.imread(path,1)
    imgGray = cv2.imread(path,0)
    return (imgColor, imgGray)

def showImg(nameWindow, matImage, t):
    cv2.imshow(nameWindow, matImage)
    cv2.waitKey(t)

if __name__ == "__main__":
    imgColor, imgGray = loadImage(path)
    showImg("imgColor", imgColor, 0)
    _red, img_cir = cv2.threshold(imgGray, 100, 255, cv2.THRESH_BINARY)
    #showImg("img_bin", img_bin, 0)
    kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT,(4,4))
    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))
    kernel3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11))

    img_cir = cv2.erode(img_cir, kernel=kernel1, iterations=2)
    showImg("img_cir", img_cir, 0)
    img_cir = cv2.dilate(img_cir, kernel=kernel3, iterations=1)
    showImg("img_cir", img_cir, 0)

    cv2.destroyAllWindows()