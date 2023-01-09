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

cv2.namedWindow('windTrack1')
cv2.createTrackbar('u1', 'windTrack1', 0, 255, nothing)        # u1 = umbral

cv2.namedWindow('windTrack2')
cv2.createTrackbar('u2', 'windTrack2', 0, 255, nothing)        # u2 = umbral

if __name__ == "__main__":
    imgColor, imgGray = loadImage(path)
    while True:
        if (cv2.waitKey(1) & 0xFF == ord ('q')):
            break
        #showImgW("imGgray", imgGray)
        u1 = cv2.getTrackbarPos('u1', 'windTrack1')
        u2 = cv2.getTrackbarPos('u2', 'windTrack2')
        imgNewColor = imgColor
        imgNewColor[:,:,0] = u1
        imgNewColor[:,:,1] = u2
        showImgW("imgNewColor", imgNewColor)
    cv2.destroyAllWindows()
