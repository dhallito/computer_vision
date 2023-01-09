#By Juan David Cuscagua López
#Para filtrar los colores de las frutas, utilicé un código que hice para la actividad 2: "rangos_colores_punto1.py"
#Vale la pena descomentar todas las lines de showImg para ver el proceso de filtro
#Profe, de las mejores materias que he visto

import numpy as np
import cv2

def loadImage (path):
    imgColor = cv2.imread(path,1)
    imgGray = cv2.imread(path,0)
    return (imgColor, imgGray)

def showImg(nameWindow, matImage, t):
    cv2.imshow(nameWindow, matImage)
    cv2.waitKey(t)

if __name__ == "__main__":
    paths = []
    img_train = []
    for i in range(32):
        paths.append("imagenes/"+str(i+1)+".jpg")

    for i in range(32):
        original_imgColor, original_imgGray = loadImage(paths[i])
        width = int(original_imgColor.shape[1] * 0.3)
        height = int(original_imgColor.shape[0] * 0.3)
        dim = (width, height)
        imgColor = cv2.resize(original_imgColor, dim, interpolation = cv2.INTER_AREA)
        imgGray = cv2.resize(original_imgGray, dim, interpolation = cv2.INTER_AREA)
        #showImg("imgColor", imgColor, 0)

        # Limones
        roi_limones = imgColor[366:416, 126:341]
        #showImg("roi_limones", roi_limones, 0)
        width = int(roi_limones.shape[1] * 0.25)
        height = int(roi_limones.shape[0])
        for i in range(4):
            img_train.append(roi_limones[0:height, i*width:(i+1)*width])
            #showImg(f"mini_roi {i}", roi_limones[0:height, i*width:(i+1)*width], 0)

        # Juguitos
        roi_juguitos = imgColor[459:579, 126:319]
        #showImg("roi_juguitos", roi_juguitos, 0)
        width = int(roi_juguitos.shape[1] * 1/3)
        height = int(roi_juguitos.shape[0]*0.5)
        for i in range(2):
            for j in range(3):
                img_train.append(roi_juguitos[i*height:(i+1)*height, j*width:(j+1)*width])
                #showImg(f"mini_roi {i}", roi_juguitos[i*height:(i+1)*height, j*width:(j+1)*width], 0)
        
        # Manzananitas
        roi_manzanitas = imgColor[695:760, 103:332]
        #showImg("roi_manzanitas", roi_manzanitas, 0)
        width = int(roi_manzanitas.shape[1] * 1/3)
        height = int(roi_manzanitas.shape[0]*1)
        for i in range(3):
            img_train.append(roi_manzanitas[0:height, i*width:(i+1)*width])
            #showImg(f"mini_roi {i}", roi_manzanitas[0:height, i*width:(i+1)*width], 0)
        
        # Repisa_1
        roi_repisa_1 = imgColor[382:471, 371:557]
        #showImg("roi_repisa_1", roi_repisa_1, 0)
        width = int(roi_repisa_1.shape[1] * 0.5)
        height = int(roi_repisa_1.shape[0]*1)
        for i in range(2):
            img_train.append(roi_repisa_1[0:height, i*width:(i+1)*width])
            #showImg(f"mini_roi {i}", roi_repisa_1[0:height, i*width:(i+1)*width], 0)

        # Repisa_2
        roi_repisa_2 = imgColor[513:610, 368:547]
        #showImg("roi_repisa_2", roi_repisa_2, 0)
        width = int(roi_repisa_2.shape[1] * 0.5)
        height = int(roi_repisa_2.shape[0]*1)
        for i in range(2):
            img_train.append(roi_repisa_2[0:height, i*width:(i+1)*width])
            #showImg(f"mini_roi {i}", roi_repisa_2[0:height, i*width:(i+1)*width], 0)

        # Repisa_3
        roi_repisa_3 = imgColor[665:765, 374:553]
        #showImg("roi_repisa_3", roi_repisa_3, 0)
        width = int(roi_repisa_3.shape[1] * 0.5)
        height = int(roi_repisa_3.shape[0]*1)
        for i in range(2):
            img_train.append(roi_repisa_3[0:height, i*width:(i+1)*width])
            #showImg(f"mini_roi {i}", roi_repisa_3[0:height, i*width:(i+1)*width], 0)
    cv2.destroyAllWindows()

    for i in range(len(img_train)):
        cv2.imwrite(f"alimentos/{i}.jpg", img_train[i])