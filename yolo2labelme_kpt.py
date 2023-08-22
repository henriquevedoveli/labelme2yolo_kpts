import os 
import glob
import cv2
import json

class Yolo2Labelme:
    def __init__(self) -> None:
        self.path = ''

    def generateLabelmeJson(self):

        self.txtFileList = glob.glob(self.datasetAnnotationPath + '*.txt')

        for arquivo in self.txtFileList:
            imagePath = arquivo.replace("txt", "png")
            imageName = os.path.basename(arquivo).replace("txt", "png")
            h_image, w_image = cv2.imread(imagePath).shape[:2]


            #Estrutura geral do Json
            jsonFile = {
            "version": "4.5.6",
            "flags": {},
            "shapes": [],
            "imagePath": imageName,
            "imageData": None,
            "imageHeight": h_image,
            "imageWidth": w_image
            }        
            shapes = []       
            dados = []
            classe = ""        

            bb = None
            shape = None

            if os.path.getsize(arquivo) > 0:
                bb = open(arquivo)

                for line in bb.readlines():

                    dadosTemp = line.split(' ')
                    
                    if dadosTemp[0] == '0':
                        classe = 'person'
                    else:
                        classe = 'personH'

                    x = int(float(dadosTemp[1])*w_image)
                    y = int(float(dadosTemp[2])*h_image)
                    w = int(float(dadosTemp[3])*w_image)
                    h = int(float(dadosTemp[4])*h_image)


                    x1 = int(x - w/2)
                    y1 = int(y - h/2)
                    x2 = int(x + w/2)
                    y2 = int(y + h/2)
                    
                    points = []

                    #Estrutura geral da anotação de detecção
                    shapeData =  {

                        "label": "",
                        "points": [],
                        "group_id": None,
                        "shape_type": shape,
                        "flags": {}
                    }            
                    
                    shapeData.update({"label" : classe})          

                    points.append([x1, y1])
                    points.append([x2, y2])

                    shapeData.update({"points" : points})
                    shapes.append(shapeData)

                    jsonFile.update({"shapes" : shapes})

                jsonPath = arquivo.replace(".txt",".json")

                with open(jsonPath, 'w+') as f:
                    f.writelines(json.dumps(jsonFile))
                f.close()