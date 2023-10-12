import numpy as np
from matplotlib import image
from matplotlib import pyplot
from DroneModel import DroneModel
from sklearn.datasets import make_blobs
from sklearn.neighbors import KernelDensity
#import cv2

# This class provides a model of a swarm of drones navigating a field
class SwarmModel: 
    def __init__ (self, fieldModel, refreshRate, time, generations, swarmSize=10, externalWeightInfluence=1e-5):
        self.fieldModel = fieldModel
        self.refreshRate = refreshRate
        self.simulationTime = refreshRate * 60 * time
        self.generations = generations
        self.swarmSize = swarmSize
        self.externalWeightInfluence=externalWeightInfluence

        startingXs = np.linspace(0, self.fieldModel.width, self.swarmSize)

        self.drones = list()
        self.flowerDict = dict()

        droneId = 0

        for x in startingXs:
            self.drones.append(DroneModel(droneId, self, np.array([x, 0.0]), self.fieldModel, self.refreshRate))
            droneId += 1

    def runSimulation(self):
        for i in range(self.generations):
            for j in range(0, int(self.simulationTime)):
                self.advanceOneFrame()

    def createDensityMap(self, flowerArr):
        # Extract all the x and y coordinates of all flowers
        x = flowerArr[:, 0]
        y = flowerArr[:, 1]

        # Concatenate x and y cordinates into a single array of shape (n_samples, n_features)
        data = np.column_stack((x, y))

        # Create a density map using KernelDensity
        kde = KernelDensity(bandwidth=1.0, kernel='gaussian')
        kde.fit(data)
        # Grid for evaluation
        xi, yi = np.mgrid[0:self.fieldModel.length:0.1, 0:self.fieldModel.width:0.1]
        xy = np.vstack([xi.ravel(), yi.ravel()]).T
        self.DensityMap = (np.exp(kde.score_samples(xy)).reshape(xi.shape)).T

    def handleNewGeneration(self):
        flowerList = []
        for flowerBytes in self.flowerDict.keys():
            flower = np.frombuffer(flowerBytes, dtype=np.float64)
            flowerList.append(flower)

        flowerArr = np.asarray(flowerList)
        self.createDensityMap(flowerArr)

    def advanceOneFrame(self):
        averageWeightedPos = [0,0]
        weightSum = 0
        for drone in self.drones:
            weightSum += drone.totalWeight
            averageWeightedPos += drone.pos * drone.totalWeight
        
        if weightSum > 0:
            averageWeightedPos = averageWeightedPos / weightSum
        else:
            averageWeightedPos = [-1, -1]
        
        for drone in self.drones:
            drone.advanceOneFrame(averageWeightedPos, self.externalWeightInfluence)

    def getFlowerDict(self):
        return self.drones[0].getFlowerDict()
    
    def getDronePositions(self):
        positions = []
        for drone in self.drones:
            positions.append(drone.pos)
        positions = np.array(positions)
        return positions
    
    def getDroneVelocities(self):
        velocities = []
        magnitudes = []
        for drone in self.drones:
            velocities.append(drone.vel)
            magnitudes.append(np.sqrt(np.sum(drone.vel*drone.vel)))
        velocities = np.array(velocities)
        magnitudes = np.array(magnitudes)

        return velocities, magnitudes
    
    def updateFlowerDict(self, effectedFlowers, cameraFlowers):
        for cameraFlower in cameraFlowers:
            if cameraFlower.tobytes() not in self.flowerDict:
                self.flowerDict[cameraFlower.tobytes()] = 0.0
        for effectedFlower in effectedFlowers:
            if effectedFlower.tobytes() in self.flowerDict:
                self.flowerDict[effectedFlower.tobytes()] = self.flowerDict[effectedFlower.tobytes()] + (1.0)/self.refreshRate
            else:
                self.flowerDict[effectedFlower.tobytes()] = (1.0)/self.refreshRate

    def getTimes(self, flowers):
        times = [self.flowerDict[flower.tobytes()] for flower in flowers]
        return times