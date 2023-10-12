from matplotlib import image
from matplotlib import pyplot
import numpy as np
import cv2

class greenHouseModel: 

    flowerdens = .005

    def getListOfPointsFromLine(self, line):
        listOfPointStrings = line.split(" ")
        stringPoints = [pointString.split(",") for pointString in listOfPointStrings]
        pointArr = [[int(num) for num in point] for point in stringPoints]
        return pointArr

    def __init__ (self, fileName = "textBasedModel.txt"):
        file = open(fileName, 'r')
        lines = file.readlines()
        lines = [line.strip('\n') for line in lines]

        dimensions = lines[0].split(" ")
        dimensions = [int(dimensions[0]), int(dimensions[1])]

        droneSpawn = lines[1].split(" ")
        self.droneSpawn = [int(droneSpawn[0]), int(droneSpawn[1])]

        polyPoints = [np.array(self.getListOfPointsFromLine(line), dtype=np.int32) for line in lines[2:]]
        img = np.zeros((dimensions[0], dimensions[1], 1), dtype = np.uint8)
        layout = img

        white = (255, 255, 255)
        isClosed = True
        thickness = 1

        for poly in polyPoints:
            layout = cv2.fillPoly(layout, np.int32([poly]), white)

        arr = np.asarray(layout)
        print(layout)
        self.planterModel = arr
        self.flowerModel = np.random.choice([0,1], np.shape(self.planterModel), p=[1 - self.flowerdens, self.flowerdens])
        self.flowerModel = self.flowerModel * self.planterModel

    def getFlowerModel(self):
        return self.flowerModel

    def getPlanterModel(self):
        return self.planterModel

