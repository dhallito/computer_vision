import cv2
import numpy as np
from glob import glob
import joblib

ct = 0.5
nmsT = 0.4

width = 320
height = 320

paths = []
img_train = []

classFile = "model.names"

classes = None

with open(classFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')
    print(classes)

pathModelCfg = 'trChar.cfg'
pathModelWei = 'trChar.weights'

net = cv2.dnn.readNetFromDarknet(pathModelCfg, pathModelWei)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

model_ss = joblib.load('model_ss.pkl')
model_svm = joblib.load('model_svm.pkl')



def decodificar(argument):
    switcher = {
        0: "0",
        1: "1",
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7",
        8: "8",
        9: "9",
        10: "E",
        11: "G",
        12: "I",
        13: "J",
        14: "K",
        15: "M",
        16: "N",
        17: "R",
        18: "S",
        19: "T",
        20: "U",
        21: "X",
        22: "Z",
    }
    return(switcher.get(argument, "Invalid month"))

# Get the names of the output layers

def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i - 1] for i in net.getUnconnectedOutLayers()]

def saveROIs(imgColor, outs, name):
    h, w = imgColor.shape[:2]
    classIds = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            # print(detection)
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]

            if confidence > ct:
                cx = int(detection[0] * w)
                cy = int(detection[1] * h)
                widthO = int(detection[2] * w)
                heightO = int(detection[3] * h)
                x1 = int(cx - widthO/2)
                y1 = int(cy - heightO/2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([x1, y1, widthO, heightO])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, ct, nmsT)
    count = 0
    for i in indices:
        
        box = boxes[i]
        x = box[0]
        y = box[1]
        W = box[2]
        H = box[3]
        x2 = x+W
        y2 = y+H
        imgRoi = imgColor[y:y2, x:x2]
        #cv2.imshow("aaaaa", imgRoi)
        #cv2.waitKey(0)
        try:
            cv2.imwrite(f"imagesRois/000{name}{count}.jpg", imgRoi)
            #cv2.imwrite(f"imagesRois/{name}{count}.jpg", imgRoi)
        except:
            pass
        count += 1
            

def postProcess(imgColor, outs):
    h, w = imgColor.shape[:2]
    classIds = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            # print(detection)
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]

            if confidence > ct:
                cx = int(detection[0] * w)
                cy = int(detection[1] * h)
                widthO = int(detection[2] * w)
                heightO = int(detection[3] * h)
                x1 = int(cx - widthO/2)
                y1 = int(cy - heightO/2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([x1, y1, widthO, heightO])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, ct, nmsT)
    for i in indices:
        box = boxes[i]
        x = box[0]
        y = box[1]
        W = box[2]
        H = box[3]
        x2 = x+W
        y2 = y+H
        if W>15:
            drawPredict(imgColor, classIds[i], confidences[i], x, y, x2, y2)


def predictChar(imgRoi):
    vector_pixel = []
    for a in cv2.resize(imgRoi,(25,50)):
        for b in a:
            vector_pixel.append(b)
    vectorCarac=np.array(vector_pixel,dtype=np.float32)
    vc_r = vectorCarac.reshape(1, -1)
    vc_ss = model_ss.transform(vc_r)
    result_predict = model_svm.predict(vc_ss)

    return result_predict[0]


def drawPredict(imgColor, classId, conf, left, top, right, bottom):
    # Draw a bounding box.
    imgRoi = imgColor[top:bottom, left:right]
    #cv2.imwrite("imagesRois/prueba.jpg", imgRoi)
    valor = decodificar(int(predictChar(imgRoi)))
    #cv2.imshow("predict Image Roi", cv2.resize(imgRoi, (480, 320)))
    #cv2.waitKey(0)
    #

    cv2.rectangle(imgColor, (left, top), (right, bottom), (0, 255, 0), 1)
    cv2.putText(imgColor,str(valor), (left,bottom+5), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (0,0,0), 1, cv2.LINE_AA)
    
    cv2.imshow("predict Image", cv2.resize(imgColor, (480, 320)))
    cv2.waitKey(0)


def main():
    for pathImg in glob('Images/test'+'/*.jpg'):
        paths.append(pathImg)

    print(len(paths))
    for i in range(len(paths)):
        imgColor = cv2.imread(paths[i], 1)
        imgGray = cv2.imread(paths[i],0)
        #cv2.imshow("aaaaa", imgColor)
        #cv2.waitKey(0)
        blob = cv2.dnn.blobFromImage(
            imgColor, 1/255, (width, height), [0, 0, 0], 1, crop=False)
        net.setInput(blob)
        
        outs = net.forward(getOutputsNames(net))
        #print(outs)
        #saveROIs(imgColor, outs, i)
        postProcess(imgGray, outs)


main()
cv2.destroyAllWindows()
