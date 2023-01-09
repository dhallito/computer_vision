import numpy as np
import cv2

path = "imagenMorph_2.png"

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
    _red, img_bin = cv2.threshold(imgGray, 100, 255, cv2.THRESH_BINARY)
    showImg("img_bin", img_bin, 0)
    '''img_GB = cv2.GaussianBlur(imgColor, (11,11), 0)
    showImg("img_GB", img_GB,0)
    img_blur = cv2.blur(imgColor, (10,10))
    showImg("img_blur", img_blur,0)
    img_median = cv2.medianBlur(imgColor, 11)
    showImg("img_median", img_median,0)'''
    '''img_canny = cv2.Canny(imgGray, 100, 200)
    showImg("img_canny", img_canny, 0)
    img_sobelx = cv2.Sobel(imgColor, cv2.CV_64F, 1, 0, ksize=11)
    showImg("img_sobelx", img_sobelx, 0)
    img_sobely = cv2.Sobel(imgColor, cv2.CV_64F, 0, 1, ksize=5)
    showImg("img_sobely", img_sobely, 0)'''
    '''kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    img_erode = cv2.erode(img_bin, kernel=kernel1, iterations=3)
    showImg("img_erode", img_erode, 0)
    img_dilate = cv2.dilate(img_bin, kernel=kernel1, iterations=1)
    showImg("img_dilate", img_dilate, 0)'''
    cv2.destroyAllWindows()


